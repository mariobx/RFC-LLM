"""Order-Sorted Message Algebra Sort Definitions for MITRE CPSA 4.4.9."""

from enum import Enum


class CPSASortEnum(str, Enum):
    """Supported sorts in MITRE CPSA order-sorted algebras (Tables 10.2, 10.4, 10.6)."""

    # Basic Atomic Sorts
    NAME = "name"      # Principal identifiers
    TEXT = "text"      # Fresh nonces and text tokens
    DATA = "data"      # Arbitrary payload / secrets
    TAG = "tag"        # Constant tag atoms
    SKEY = "skey"      # Symmetric encryption keys
    AKEY = "akey"      # Asymmetric keys (public or private)
    DEV = "dev"        # Hardware device identifiers
    CHAN = "chan"      # Communication channels (required by cpsa4roletran)
    LOCN = "locn"      # State memory locations (doors / envelopes)
    MESG = "mesg"      # Top sort (any valid message)

    # Diffie-Hellman Algebra Sorts
    RNDX = "rndx"      # Random exponents (must be uniquely originating)
    EXPT = "expt"      # Exponent expressions

    # Logic & Rule Sorts
    FACT = "fact"      # User-defined facts
    STRD = "strd"      # Strand index in rules/goals
    INDX = "indx"      # Node height index in rules/goals
