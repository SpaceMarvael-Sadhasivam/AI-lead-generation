"""
Router for Course Lead Qualification Agent

Purpose:
- Map policy actions → response template keys
- No business logic
- No decision-making
"""

from agent.policy_engine import PolicyAction


class Router:
    def route(self, action):
        """
        Translate a PolicyAction into a response template key.
        """

        if action == PolicyAction.ASK_DISCOVERY:
            return self._discovery_route()

        if action == PolicyAction.PROVIDE_INFORMATION:
            return "offer_information"

        if action == PolicyAction.HANDOFF:
            return "handoff"

        if action == PolicyAction.POLITE_EXIT:
            return "polite_exit"

        return "fallback"

    # ----------------------------------------------------

    def _discovery_route(self):
        """
        Decide which discovery question to ask next.
        This is intentionally simple.
        State-based refinement can be added later.
        """
        return "discovery_interest"
