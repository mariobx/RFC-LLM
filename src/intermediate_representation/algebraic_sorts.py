"""Order-Sorted Message Algebra Sort Definitions for MITRE CPSA 4.4.9.

Grounded directly in MITRE CPSA 4.4.9 User Manual Tables 7.1, 10.2, 10.4, and 10.6,
and CPSA4 Roletran (`Role_Translations.md` Section 2).
"""

from enum import Enum
from typing import Set


class CPSASortEnum(str, Enum):
    """Supported sorts in MITRE CPSA 4.4.9 order-sorted algebras and logic rules."""

    # Basic Message Algebra Sorts (Table 10.2)
    NAME = "name"      # Principal identifiers (required by pubk, privk, ltk, bltk)
    TEXT = "text"      # Fresh nonces and plain text tokens
    DATA = "data"      # Arbitrary payload / secrets
    TAG = "tag"        # Constant tag atoms
    SKEY = "skey"      # Symmetric encryption keys
    AKEY = "akey"      # Asymmetric keys (public or private)
    DEV = "dev"        # Hardware device identifiers
    CHAN = "chan"      # Communication channels (required by cpsa4roletran)
    LOCN = "locn"      # State memory locations (load / stor events)
    MESG = "mesg"      # Universal top sort (cannot be an encryption key per Eq. 10.1)

    # Diffie-Hellman Message Algebra Sorts (Table 10.4)
    RNDX = "rndx"      # Atomic random exponents (must be uniq-gen, never uniq-orig)
    EXPT = "expt"      # Compound exponent expressions (rndx < expt < mesg)
    BASE = "base"      # Diffie-Hellman group base elements

    # First-Order Logic & Goal Sorts (Table 7.1 — forbidden in role/skeleton vars)
    FACT = "fact"      # User-defined relational facts
    STRD = "strd"      # Strand variable sort in defrule/defgoal quantifiers
    INDX = "indx"      # Node index sort in defrule/defgoal quantifiers


# Sorts permitted inside (vars ...) of defrole and defskeleton under 'basic' algebra (Table 10.2)
CPSA_BASIC_VARIABLE_SORTS: Set[str] = {
    CPSASortEnum.NAME.value,
    CPSASortEnum.TEXT.value,
    CPSASortEnum.DATA.value,
    CPSASortEnum.TAG.value,
    CPSASortEnum.SKEY.value,
    CPSASortEnum.AKEY.value,
    CPSASortEnum.DEV.value,
    CPSASortEnum.CHAN.value,
    CPSASortEnum.LOCN.value,
    CPSASortEnum.MESG.value,
}

# Additional sorts permitted inside (vars ...) only under 'diffie-hellman' algebra (Table 10.4)
CPSA_DH_ONLY_VARIABLE_SORTS: Set[str] = {
    CPSASortEnum.RNDX.value,
    CPSASortEnum.EXPT.value,
    CPSASortEnum.BASE.value,
}

# Complete set of sorts permitted in (vars ...) declarations of defrole and defskeleton
CPSA_ALL_VARIABLE_SORTS: Set[str] = CPSA_BASIC_VARIABLE_SORTS | CPSA_DH_ONLY_VARIABLE_SORTS

# First-order logic sorts restricted exclusively to defrule / defgoal quantifiers (Table 7.1)
CPSA_LOGIC_ONLY_SORTS: Set[str] = {
    CPSASortEnum.FACT.value,
    CPSASortEnum.STRD.value,
    CPSASortEnum.INDX.value,
}

# Basic Value sorts (BV_X) permitted in cpsa4roletran (inputs ...) declarations alongside channels
CPSA_BASIC_VALUE_SORTS: Set[str] = {
    CPSASortEnum.NAME.value,
    CPSASortEnum.TEXT.value,
    CPSASortEnum.DATA.value,
    CPSASortEnum.TAG.value,
    CPSASortEnum.SKEY.value,
    CPSASortEnum.AKEY.value,
    CPSASortEnum.DEV.value,
    CPSASortEnum.LOCN.value,
}
