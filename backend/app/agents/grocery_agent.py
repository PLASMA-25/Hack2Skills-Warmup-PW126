from pydantic import BaseModel, Field

from app.models.meal_plan import GroceryAgentInput, GroceryAgentOutput, GroceryItem
from app.services.llm import structured_completion

SYSTEM_PROMPT = """You build a consolidated grocery shopping list from planned meals.
Deduplicate ingredients, specify quantities for the serving count, and estimate cost per item in the given currency.
Be realistic with grocery prices."""


class GroceryListWrapper(BaseModel):
    items: list[GroceryItem] = Field(description="Consolidated grocery items")


def build_grocery_list(payload: GroceryAgentInput) -> GroceryAgentOutput:
    meals_text = "\n".join(
        f"{slot}: {meal.name} — {', '.join(meal.ingredients)}"
        for slot, meal in payload.meals.items()
    )
    user_prompt = (
        f"Servings: {payload.servings}\n"
        f"Currency: {payload.currency}\n"
        f"Meals:\n{meals_text}\n"
        "Return consolidated grocery list with item, quantity, estimated_cost."
    )
    result = structured_completion(SYSTEM_PROMPT, user_prompt, GroceryListWrapper)
    return GroceryAgentOutput(items=result.items)
