from typing import Literal

from app.config import settings
from app.graph.state import GraphState


def route_after_validate(state: GraphState) -> Literal["supervisor_clarify", "init_meal_queue"]:
    if state.get("missing_fields"):
        return "supervisor_clarify"
    return "init_meal_queue"


def route_after_meal(state: GraphState) -> Literal["plan_next_meal", "grocery"]:
    if state.get("pending_meal_slots"):
        return "plan_next_meal"
    return "grocery"


def route_after_budget(state: GraphState) -> Literal["retry_budget", "finalize"]:
    result = state.get("budget_result")
    retries = state.get("retries", 0)
    if result and not result.within_budget and retries < settings.max_budget_retries:
        return "retry_budget"
    return "finalize"
