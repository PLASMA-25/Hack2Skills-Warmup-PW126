from typing import Literal

from pydantic import BaseModel, Field

from app.models.intent import MealSlot, ParsedIntent


class Meal(BaseModel):
    name: str = Field(description="Name of the dish")
    description: str = Field(description="Short description of the meal")
    ingredients: list[str] = Field(description="Ingredients with approximate quantities")
    prep_time_min: int = Field(ge=1, description="Estimated prep and cook time in minutes")


class GroceryItem(BaseModel):
    item: str
    quantity: str
    estimated_cost: float = Field(ge=0)


class Substitution(BaseModel):
    original: str
    alternative: str
    reason: str


class BudgetResult(BaseModel):
    estimated_total: float = Field(ge=0)
    limit: float = Field(ge=0)
    within_budget: bool
    notes: str


class MealAgentInput(BaseModel):
    slot: MealSlot
    intent: ParsedIntent
    budget: float
    currency: str
    reduce_cost: bool = False


class MealAgentOutput(BaseModel):
    slot: MealSlot
    meal: Meal


class GroceryAgentInput(BaseModel):
    meals: dict[str, Meal]
    servings: int
    currency: str


class GroceryAgentOutput(BaseModel):
    items: list[GroceryItem]


class SubstitutionsAgentInput(BaseModel):
    grocery_list: list[GroceryItem]
    intent: ParsedIntent
    budget: float
    currency: str


class SubstitutionsAgentOutput(BaseModel):
    substitutions: list[Substitution]


class BudgetAgentInput(BaseModel):
    grocery_list: list[GroceryItem]
    budget: float
    currency: str


class BudgetAgentOutput(BaseModel):
    result: BudgetResult


class SupervisorInput(BaseModel):
    missing_fields: list[str]
    field_metadata: list[dict[str, str]]
    partial_intent: ParsedIntent
    user_intent: str


class SupervisorOutput(BaseModel):
    question: str


class FillFieldsInput(BaseModel):
    partial_intent: ParsedIntent
    clarification_answer: str
    missing_fields: list[str]
    user_intent: str


class IntentExtractInput(BaseModel):
    user_intent: str
    budget: float
    currency: str


class PlanRequest(BaseModel):
    user_intent: str = Field(min_length=1, max_length=2000)
    budget: float = Field(gt=0, le=10000)
    currency: str = Field(default="USD", min_length=3, max_length=3)
    partial_intent: ParsedIntent | None = None
    clarification_answer: str | None = Field(default=None, max_length=500)


class ClarificationPrompt(BaseModel):
    question: str
    missing_fields: list[str]
    partial_intent: ParsedIntent


class PlanResult(BaseModel):
    parsed_intent: ParsedIntent
    meals: dict[str, Meal]
    grocery_list: list[GroceryItem]
    substitutions: list[Substitution]
    budget: BudgetResult
    retries: int = 0


class PlanResponse(BaseModel):
    status: Literal["needs_clarification", "complete"]
    clarification: ClarificationPrompt | None = None
    plan: PlanResult | None = None
