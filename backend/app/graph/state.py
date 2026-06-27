from typing import Literal, TypedDict

from app.models.intent import MealSlot, ParsedIntent
from app.models.meal_plan import BudgetResult, GroceryItem, Meal, Substitution


class GraphState(TypedDict, total=False):
    user_intent: str
    budget: float
    currency: str
    partial_intent: ParsedIntent | None
    clarification_answer: str | None
    parsed_intent: ParsedIntent | None
    missing_fields: list[str]
    clarification_question: str | None
    pending_meal_slots: list[MealSlot]
    meals: dict[str, Meal]
    grocery_list: list[GroceryItem]
    substitutions: list[Substitution]
    budget_result: BudgetResult | None
    retries: int
    reduce_cost: bool
    status: Literal["needs_clarification", "complete", "planning"]
