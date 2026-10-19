"""Asynchronous web server for live RFC-to-CPSA synthesis visualization."""

import asyncio
import json
import logging
from pathlib import Path
from typing import Set
from aiohttp import web

from src.system_config import SYSTEM_CONFIG
from src.pipeline_events import GLOBAL_EVENT_BUS, PipelineEvent

logger = logging.getLogger("rfc_llm.visualizer")

HTML_TEMPLATE_PATH = Path(__file__).parent / "static" / "index.html"


class VisualizerServer:
    """Manages SSE streaming, artifact serving, and dashboard state."""

    def __init__(self, host: str = "127.0.0.1", port: int = 8080):
        self.host = host
        self.port = port
        self.app = web.Application()
        self._sse_clients: Set[asyncio.Queue] = set()
        self._setup_routes()

        # Connect event bus to SSE clients
        GLOBAL_EVENT_BUS.subscribe(self._on_bus_event)

    def _setup_routes(self):
        self.app.router.add_get("/", self.handle_index)
        self.app.router.add_get("/api/events", self.handle_sse)
        self.app.router.add_get("/api/history", self.handle_history)
        self.app.router.add_get("/api/artifact", self.handle_artifact)
        self.app.router.add_static("/output", SYSTEM_CONFIG.DEFAULT_OUTPUT_DIR, show_index=True)

    def _on_bus_event(self, event: PipelineEvent):
        """Dispatches an event from the pipeline event bus to all connected web clients thread-safely."""
        if hasattr(self, "loop") and self.loop and self.loop.is_running():
            for q in list(self._sse_clients):
                try:
                    self.loop.call_soon_threadsafe(q.put_nowait, event)
                except Exception:
                    pass
        else:
            for q in list(self._sse_clients):
                try:
                    q.put_nowait(event)
                except Exception:
                    pass

    async def handle_index(self, request: web.Request) -> web.Response:
        """Serves the main single-page visualizer dashboard."""
        if not HTML_TEMPLATE_PATH.exists():
            return web.Response(text="Dashboard template not found.", status=404)
        with open(HTML_TEMPLATE_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        return web.Response(text=content, content_type="text/html")

    async def handle_history(self, request: web.Request) -> web.Response:
        """Returns JSON array of past events for state reconstruction on page load."""
        history = [e.model_dump() for e in GLOBAL_EVENT_BUS.get_history()]
        return web.json_response(history)

    async def handle_artifact(self, request: web.Request) -> web.Response:
        """Serves synthesized code or MITRE verification output files."""
        filepath_str = request.query.get("path")
        if not filepath_str:
            return web.Response(text="Missing 'path' parameter", status=400)

        path = Path(filepath_str).resolve()
        if not path.exists():
            return web.Response(text=f"Artifact not found: {path}", status=404)

        # Content-type detection
        content_type = "text/plain"
        if path.suffix == ".xhtml" or path.suffix == ".html":
            content_type = "application/xhtml+xml"
        elif path.suffix == ".svg":
            content_type = "image/svg+xml"
        elif path.suffix == ".json":
            content_type = "application/json"
        elif path.suffix == ".scm":
            content_type = "text/plain"

        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            body = f.read()

        return web.Response(text=body, content_type=content_type)

    async def handle_sse(self, request: web.Request) -> web.StreamResponse:
        """Streams live Server-Sent Events to dashboard clients."""
        response = web.StreamResponse(
            status=200,
            reason="OK",
            headers={
                "Content-Type": "text/event-stream",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*",
            },
        )
        await response.prepare(request)

        client_queue: asyncio.Queue = asyncio.Queue()
        self._sse_clients.add(client_queue)

        # Initial ping
        await response.write(b": ping\n\n")

        try:
            while True:
                try:
                    event: PipelineEvent = await asyncio.wait_for(client_queue.get(), timeout=15.0)
                    sse_msg = event.to_sse_message().encode("utf-8")
                    await response.write(sse_msg)
                except asyncio.TimeoutError:
                    # Keep-alive heartbeat
                    await response.write(b": heartbeat\n\n")
        except (asyncio.CancelledError, ConnectionResetError):
            pass
        finally:
            self._sse_clients.discard(client_queue)

        return response


def run_visualizer_in_background(host: str = "127.0.0.1", port: int = 8080):
    """Starts the visualizer server in a background daemon thread."""
    import threading
    import socket
    import time

    def _is_port_available(p: int) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex((host, p)) != 0

    actual_port = port
    while not _is_port_available(actual_port) and actual_port < port + 20:
        actual_port += 1

    server = VisualizerServer(host=host, port=actual_port)
    server.port = actual_port

    def _target():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        server.loop = loop
        runner = web.AppRunner(server.app)
        loop.run_until_complete(runner.setup())
        site = web.TCPSite(runner, host, actual_port)
        loop.run_until_complete(site.start())
        logger.info("Visualizer server active at http://%s:%d", host, actual_port)
        loop.run_forever()

    t = threading.Thread(target=_target, daemon=True)
    t.start()
    time.sleep(0.15)
    return server
