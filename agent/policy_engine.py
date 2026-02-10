"""
Policy Engine for Course Lead Qualification Agent

Purpose:
- Enforce qualification-first behavior
- Prevent early selling or urgency
- Decide next action based on intent + state
"""

from agent.intent import Intent


class PolicyAction:
    ASK_DISCOVERY = "ask_discovery"
    PROVIDE_INFORMATION = "provide_information"
    HANDOFF = "handoff"
    POLITE_EXIT = "polite_exit"
    FALLBACK = "fallback"


class PolicyEngine:
    """
    This class decides WHAT the agent is allowed to do next.
    It does NOT generate text. It only enforces rules.
    """

    def decide_next_action(self, intent, state):
        """
        Determine next action based on intent and current lead state.
        """

        # ---- HARD STOPS (non-negotiable) ----

        if intent == Intent.NOT_INTERESTED:
            state.interest_level = "cold"
            state.qualification_complete = True
            return PolicyAction.POLITE_EXIT

        # ---- DECISION AUTHORITY CHECK ----

        if intent == Intent.NEEDS_DECISION_SUPPORT:
            state.decision_maker = "parents"
            # Never sell or handoff when parents decide
            return PolicyAction.PROVIDE_INFORMATION

        # ---- PRICE SENSITIVITY ----

        if intent == Intent.PRICE_SENSITIVE:
            state.budget_sensitivity = "high"
            state.interest_level = state.interest_level or "warm"
            # Price-sensitive users must never be pushed
            return PolicyAction.PROVIDE_INFORMATION

        # ---- EXPLORATION / EARLY STAGE ----

        if intent in (Intent.PARTIALLY_INTERESTED, Intent.ASKING_DETAILS):
            state.interest_level = "warm"
            state.qualification_complete = False
            return PolicyAction.ASK_DISCOVERY

        # ---- STRONG INTEREST ----

        if intent == Intent.INTERESTED:
            # INTERESTED does NOT mean ready for handoff
            state.interest_level = "warm"
            return PolicyAction.ASK_DISCOVERY

        # ---- HANDOFF ELIGIBILITY (VERY STRICT) ----

        if intent == Intent.READY_FOR_COUNSELLOR:
            if self._handoff_allowed(state):
                state.handoff_ready = True
                state.qualification_complete = True
                return PolicyAction.HANDOFF
            else:
                # Not enough information yet
                return PolicyAction.ASK_DISCOVERY

        # ---- FALLBACK ----

        return PolicyAction.FALLBACK

    # ------------------------------------------------------------------

    def _handoff_allowed(self, state):
        """
        Handoff is allowed ONLY if:
        - Qualification is complete
        - Interest is hot
        - User is decision-maker OR explicitly asked for counsellor
        """

        if not state.qualification_complete:
            return False

        if state.interest_level != "hot":
            return False

        # Parents as decision-makers are allowed ONLY
        # when the user explicitly asks for counsellor
        return True
