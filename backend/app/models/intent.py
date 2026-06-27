from enum import StrEnum

from pydantic import BaseModel, Field


class MealSlot(StrEnum):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"


class ParsedIntent(BaseModel):
    meal_slots: list[MealSlot] | None = Field(
        None,
        description="Which meals to plan: breakfast, lunch, and/or dinner",
    )
    servings: int | None = Field(
        None,
        ge=1,
        le=20,
        description="How many people you are cooking for",
    )
    cuisine_theme: str | None = Field(
        None,
        description="Preferred cuisine or regional style such as North Indian or Italian",
    )
    diet: str | None = Field(
        None,
        description="Dietary preference such as vegetarian, vegan, or gluten-free",
    )
    constraints: list[str] = Field(
        default_factory=list,
        description="Other constraints such as quick, budget-friendly, or low spice",
    )
    day_context: str | None = Field(
        None,
        description="Context about the day such as busy workday or weekend brunch",
    )
