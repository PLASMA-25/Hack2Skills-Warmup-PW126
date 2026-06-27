from app.models.meal_plan import BudgetAgentInput, BudgetAgentOutput, BudgetResult
from app.services.llm import structured_completion

SYSTEM_PROMPT = """You evaluate whether a grocery list fits within a budget.
Sum estimated costs, compare to the limit, set within_budget true or false, and add brief notes.
If slightly over, still report accurately."""


def check_budget(payload: BudgetAgentInput) -> BudgetAgentOutput:
    items_text = "\n".join(
        f"- {item.item}: {item.estimated_cost} {payload.currency}" for item in payload.grocery_list
    )
    user_prompt = (
        f"Budget limit: {payload.budget} {payload.currency}\n"
        f"Grocery items:\n{items_text}\n"
        "Return estimated_total, limit, within_budget, notes."
    )

    class BudgetWrapper(BudgetResult):
        pass

    result = structured_completion(SYSTEM_PROMPT, user_prompt, BudgetResult)
    result = result.model_copy(update={"limit": payload.budget})
    return BudgetAgentOutput(result=result)
