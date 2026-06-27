from pydantic import BaseModel, Field

from app.models.meal_plan import (
    Substitution,
    SubstitutionsAgentInput,
    SubstitutionsAgentOutput,
)
from app.services.llm import structured_completion

SYSTEM_PROMPT = """You suggest ingredient substitutions for a grocery list.
Offer practical alternatives for dietary needs, availability, or budget savings.
Provide original ingredient, alternative, and reason for each substitution."""


class SubstitutionsWrapper(BaseModel):
    substitutions: list[Substitution] = Field(description="Suggested substitutions")


def suggest_substitutions(payload: SubstitutionsAgentInput) -> SubstitutionsAgentOutput:
    items_text = "\n".join(
        f"- {item.item} ({item.quantity}, ~{item.estimated_cost} {payload.currency})"
        for item in payload.grocery_list
    )
    user_prompt = (
        f"Diet: {payload.intent.diet or 'none'}\n"
        f"Constraints: {', '.join(payload.intent.constraints) or 'none'}\n"
        f"Budget: {payload.budget} {payload.currency}\n"
        f"Grocery list:\n{items_text}\n"
        "Suggest 3-6 helpful substitutions."
    )
    result = structured_completion(SYSTEM_PROMPT, user_prompt, SubstitutionsWrapper)
    return SubstitutionsAgentOutput(substitutions=result.substitutions)
