from dataclasses import dataclass
from typing import Optional

@dataclass
class LeadState:
    # ---- LEAD PROFILE ----
    course_interest: Optional[str] = None
    education_level: Optional[str] = None
    current_status: Optional[str] = None  # student / working / exploring
    experience_level: Optional[str] = None  # beginner / intermediate / advanced
    learning_goal: Optional[str] = None  # exploration / build / career
    
    # ---- CONSTRAINTS ----
    budget_range: Optional[str] = None
    budget_sensitivity: Optional[str] = None  # high / medium / low
    timeline: Optional[str] = None
    decision_maker: Optional[str] = None  # self / parents
    delivery_mode: Optional[str] = None  # online / offline / hybrid

    # ---- QUALIFICATION STATUS ----
    interest_level: Optional[str] = None  # hot / warm / cold
    qualification_complete: bool = False
    handoff_ready: bool = False
