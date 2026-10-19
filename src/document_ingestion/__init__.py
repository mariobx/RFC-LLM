"""Document Ingestion package for Stage 1 RFC filtering, TOC parsing, section routing, and slicing."""

from src.document_ingestion.handshake_section_router import (
    ROUTER_SYSTEM_PROMPT,
    SectionRoutingDecision,
    route_handshake_sections,
)
from src.document_ingestion.protocol_applicability_gate import (
    GATEKEEPER_SYSTEM_PROMPT,
    ProtocolApplicabilityReport,
    evaluate_protocol_applicability,
)
from src.document_ingestion.rfc_header_filter import (
    HeaderFilterResult,
    filter_rfc_header,
)
from src.document_ingestion.rfc_toc_parser import (
    TOCSectionEntry,
    parse_table_of_contents,
)
from src.document_ingestion.verbatim_section_slicer import slice_verbatim_sections

__all__ = [
    "HeaderFilterResult",
    "filter_rfc_header",
    "TOCSectionEntry",
    "parse_table_of_contents",
    "ProtocolApplicabilityReport",
    "GATEKEEPER_SYSTEM_PROMPT",
    "evaluate_protocol_applicability",
    "SectionRoutingDecision",
    "ROUTER_SYSTEM_PROMPT",
    "route_handshake_sections",
    "slice_verbatim_sections",
]
