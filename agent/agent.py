"""
Course Lead Qualification Agent
Final version – aligned to real admissions conversation
Skills + projects focused, monetisation implied
"""

from enum import Enum
import re


class ConversationState(Enum):
    OPENING = "opening"
    DISCOVERY = "discovery"
    VALUE_PITCH = "value_pitch"
    ALIGNMENT = "alignment"
    EXPLORATION = "exploration"
    LOGISTICS_PRICE = "logistics_price"
    PRICE_OBJECTION = "price_objection"
    SOFT_COMMIT = "soft_commit"
    CLOSE = "close"


class CourseLeadAgent:
    def __init__(self, memory, policy_engine, router):
        self.memory = memory
        self.policy = policy_engine
        self.router = router

        self.state = ConversationState.OPENING
        self.context = {}

    # --------------------------------------------------
    # ENTRY POINT
    # --------------------------------------------------

    def handle_input(self, user_text: str) -> str:
        text = self._normalize(user_text)
        self.memory.add_message("user", user_text)

        # 🚨 HARD EXIT — ABSOLUTE PRIORITY
        if self._is_hard_no(text):
            self.state = ConversationState.CLOSE
            response = (
                "Understood. Thanks for being upfront. "
                "I appreciate your time. Have a great day."
            )
            self.memory.add_message("agent", response)
            return response

        if self.state == ConversationState.OPENING:
            response = self._opening(text)

        elif self.state == ConversationState.DISCOVERY:
            response = self._discovery(text)

        elif self.state == ConversationState.VALUE_PITCH:
            response = self._value_pitch()

        elif self.state == ConversationState.ALIGNMENT:
            response = self._alignment(text)

        elif self.state == ConversationState.EXPLORATION:
            response = self._exploration(text)

        elif self.state == ConversationState.LOGISTICS_PRICE:
            response = self._logistics_price()

        elif self.state == ConversationState.PRICE_OBJECTION:
            response = self._price_objection(text)

        elif self.state == ConversationState.SOFT_COMMIT:
            response = self._soft_commit(text)

        else:
            response = self._close()

        self.memory.add_message("agent", response)
        return response

    # --------------------------------------------------
    # STATES
    # --------------------------------------------------

    def _opening(self, text: str) -> str:
        if self._is_yes(text):
            self.state = ConversationState.DISCOVERY
            return (
                "Great. I’d love to understand you a bit better. "
                "What do you currently do, and do you have any experience with AI tools?"
            )

        if self._is_soft_no(text):
            self.state = ConversationState.CLOSE
            return (
                "No worries at all. Thanks for letting me know. "
                "We can always connect at a better time."
            )

        return "Just to confirm, is this a good time to talk?"

    # --------------------------------------------------

    def _discovery(self, text: str) -> str:
        self.context["discovery"] = text
        self.state = ConversationState.VALUE_PITCH
        return self._value_pitch()

    # --------------------------------------------------

    def _value_pitch(self) -> str:
        self.state = ConversationState.ALIGNMENT
        return (
            "Perfect. Based on what you’ve shared, our AI Generalized Accelerator "
            "is designed exactly for this stage. Over three months plus year-long support, "
            "you’ll learn practical AI tools, build real projects like voice agents and automated workflows, "
            "and gain strong hands-on experience that you can apply confidently."
        )

    # --------------------------------------------------

    def _alignment(self, text: str) -> str:
        if self._is_yes(text):
            self.state = ConversationState.LOGISTICS_PRICE
            return self._logistics_price()

        if self._is_exploring(text):
            self.state = ConversationState.EXPLORATION
            return (
                "That makes sense. A lot of students feel the same way when they’re exploring, "
                "especially during holidays. What part are you most unsure about right now?"
            )

        return (
            "Does building practical AI skills through hands-on projects sound aligned "
            "with what you’re looking for?"
        )

    # --------------------------------------------------

    def _exploration(self, text: str) -> str:
        self.context["exploration"] = text
        self.state = ConversationState.LOGISTICS_PRICE
        return self._logistics_price()

    # --------------------------------------------------

    def _logistics_price(self) -> str:
        self.state = ConversationState.PRICE_OBJECTION
        return (
            "Just to give you clarity on the structure — the next batch onboarding is on 20 June, "
            "and classes start on 23 June. The total investment is ₹14,999, "
            "with a ₹4,999 booking amount and flexible EMI options. "
            "You also get immediate access to AI tools included with the program. "
            "Do these dates and the structure work for you?"
        )

    # --------------------------------------------------

    def _price_objection(self, text: str) -> str:
        if self._is_price_concern(text):
            self.state = ConversationState.SOFT_COMMIT
            return (
                "I completely understand — especially as a student, that’s a valid concern. "
                "That’s why we keep the booking amount low and offer EMI options, "
                "so you don’t have to decide everything upfront. "
                "Would you like me to hold a seat for 24 hours so you can discuss it comfortably?"
            )

        if self._is_yes(text):
            self.state = ConversationState.SOFT_COMMIT
            return (
                "Great. Would you like me to hold a seat for 24 hours so you can review everything "
                "and decide without any pressure?"
            )

        return (
            "Totally fair. Take your time — would you like me to hold a seat?"
        )

    # --------------------------------------------------

    def _soft_commit(self, text: str) -> str:
        if self._is_yes(text):
            self.state = ConversationState.CLOSE
            return (
                "Perfect. I’ll hold your seat for the next 24 hours. "
                "Please feel free to reach out once you’ve discussed it. "
                "Thanks so much for your time today."
            )

        self.state = ConversationState.CLOSE
        return (
            "No problem at all. I really appreciate you taking the call. "
            "Feel free to reach out anytime if you’d like to explore this further."
        )

    # --------------------------------------------------

    def _close(self) -> str:
        return "Thanks again for your time. Have a great day ahead."

    # --------------------------------------------------
    # HELPERS
    # --------------------------------------------------

    def _normalize(self, text: str) -> str:
        return re.sub(r"[^\w\s]", "", text.lower()).strip()

    def _is_yes(self, text: str) -> bool:
        return any(
            k in text for k in
            ["yes", "yeah", "sure", "ok", "okay"]
        )

    def _is_soft_no(self, text: str) -> bool:
        return any(
            k in text for k in
            ["not now", "busy", "later"]
        )

    def _is_hard_no(self, text: str) -> bool:
        return any(
            k in text for k in
            ["not interested", "no interest", "dont want", "do not want"]
        )

    def _is_exploring(self, text: str) -> bool:
        return any(
            k in text for k in
            ["too early", "exploring", "not sure", "thinking", "holidays"]
        )

    def _is_price_concern(self, text: str) -> bool:
        return any(
            k in text for k in
            ["expensive", "cost", "price", "too much", "not affordable", "student"]
        )
