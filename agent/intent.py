from enum import Enum, auto


class Intent(Enum):
    # ---- POSITIVE / NEUTRAL ----
    INTERESTED = auto()              # Clear curiosity or engagement
    PARTIALLY_INTERESTED = auto()    # Exploring, unsure, early-stage
    ASKING_DETAILS = auto()          # Wants clarity, examples, outcomes

    # ---- OBJECTIONS / CONSTRAINTS ----
    PRICE_SENSITIVE = auto()         # Cost concern
    TIMELINE_LATER = auto()          # Not now, maybe later
    NEEDS_DECISION_SUPPORT = auto()  # Parents / guardian involved

    # ---- READINESS ----
    READY_FOR_COUNSELLOR = auto()    # Explicitly asks to talk to admissions

    # ---- NEGATIVE ----
    NOT_INTERESTED = auto()           # Explicit disinterest

    # ---- FALLBACK ----
    UNKNOWN = auto()
