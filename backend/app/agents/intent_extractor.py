from app.models.intent import ParsedIntent
from app.models.meal_plan import IntentExtractInput
from app.services.llm import structured_completion

SYSTEM_PROMPT = """You extract structured cooking intent from user messages.
Set fields to null when not clearly stated or inferable — do not guess servings.
You may infer meal_slots from context (e.g. "dinner" -> ["dinner"]).
If the user is vague ("help me cook today"), infer all three meals: breakfast, lunch, dinner.
Infer diet from phrases like veg/vegetarian. Extract cuisine_theme when mentioned."""


def extract_intent(payload: IntentExtractInput) -> ParsedIntent:
    user_prompt = (
        f"User intent: {payload.user_intent}\n"
        f"Budget: {payload.budget} {payload.currency}\n"
        "Return structured intent. Use null for unknown fields."
    )
    return structured_completion(SYSTEM_PROMPT, user_prompt, ParsedIntent)
