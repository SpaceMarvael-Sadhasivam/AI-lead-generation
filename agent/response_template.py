"""
Response templates for Course Lead Qualification Voice Agent

Principles:
- No selling
- No pricing unless explicitly allowed by policy
- No urgency
- Discovery-first, human tone
- Respect student + parent decision context
"""

RESPONSES = {

    # ---- OPENING ----
    "opening": (
        "Hello {name}, this is {agent_name} calling from {organization}. "
        "I noticed you attended the {event_name} recently. "
        "I wanted to understand your experience there. "
        "Is this a good time to talk?"
    ),

    # ---- DISCOVERY ----
    "discovery_interest": (
        "What made you attend that session? "
        "Were you mainly exploring AI out of curiosity, "
        "or thinking about how it might help you in the future?"
    ),

    "discovery_background": (
        "That makes sense. Since you're early in your studies, "
        "are you mostly exploring different fields right now, "
        "or do you already have some idea of where you'd like to head?"
    ),

    "discovery_goal": (
        "When you think about learning AI, what sounds more interesting to you right now — "
        "understanding the basics, building small projects, "
        "or just getting clarity on career options?"
    ),

    # ---- CLARIFICATION (NO SELLING) ----
    "clarify_exploration": (
        "That’s completely fair. At this stage, many students are just exploring "
        "and trying to understand what’s worth learning before committing to anything."
    ),

    # ---- DECISION AUTHORITY ----
    "decision_authority": (
        "Just to make sure I guide you correctly — "
        "for longer programs or paid courses, do you usually decide on your own, "
        "or would you involve your parents?"
    ),

    # ---- SOFT VALUE (NO PRICE, NO COMMITMENT) ----
    "soft_value": (
        "In that case, what usually helps students like you is first understanding "
        "what skills are worth focusing on and what kind of outcomes are realistic, "
        "before thinking about any specific program."
    ),

    "offer_information": (
        "Would it be helpful if I shared a simple overview of "
        "what students at your stage typically focus on in AI, "
        "so you can explore it at your own pace?"
    ),

    # ---- HANDOFF (ONLY WHEN POLICY ALLOWS) ----
    "handoff": (
        "Thanks for sharing all of that. "
        "I’ll pass this information to our admissions team, "
        "and they can guide you further whenever you feel ready."
    ),

    # ---- POLITE EXIT ----
    "polite_exit": (
        "No problem at all. Thanks for your time. "
        "Feel free to reach out anytime if you’d like guidance in the future. "
        "Have a great day!"
    ),

    # ---- FALLBACK ----
    "fallback": (
        "That’s a good question. Let me rephrase that so I understand you better."
    )
}
