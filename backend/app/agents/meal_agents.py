from app.models.intent import MealSlot
from app.models.meal_plan import Meal, MealAgentInput, MealAgentOutput
from app.services.llm import structured_completion

MEAL_SYSTEM = """You are a specialized meal planning chef.
Create one realistic, cookable meal for the given meal slot.
Include dish name, description, ingredients with quantities for the serving count, and prep time.
Respect diet, cuisine, constraints, and day context. Keep costs reasonable for the budget."""


def _plan_meal(payload: MealAgentInput) -> MealAgentOutput:
    reduce_note = " Reduce ingredient costs and suggest economical dishes." if payload.reduce_cost else ""
    intent = payload.intent
    user_prompt = (
        f"Meal slot: {payload.slot.value}\n"
        f"Servings: {intent.servings}\n"
        f"Cuisine: {intent.cuisine_theme or 'any'}\n"
        f"Diet: {intent.diet or 'none'}\n"
        f"Constraints: {', '.join(intent.constraints) or 'none'}\n"
        f"Day context: {intent.day_context or 'none'}\n"
        f"Budget limit: {payload.budget} {payload.currency}{reduce_note}\n"
        "Return meal with name, description, ingredients list, prep_time_min."
    )

    class MealOnly(Meal):
        pass

    class SlotMealOutput(MealAgentOutput):
        pass

    result = structured_completion(MEAL_SYSTEM, user_prompt, Meal)
    return MealAgentOutput(slot=payload.slot, meal=result)


def plan_breakfast(payload: MealAgentInput) -> MealAgentOutput:
    return _plan_meal(payload.model_copy(update={"slot": MealSlot.BREAKFAST}))


def plan_lunch(payload: MealAgentInput) -> MealAgentOutput:
    return _plan_meal(payload.model_copy(update={"slot": MealSlot.LUNCH}))


def plan_dinner(payload: MealAgentInput) -> MealAgentOutput:
    return _plan_meal(payload.model_copy(update={"slot": MealSlot.DINNER}))
