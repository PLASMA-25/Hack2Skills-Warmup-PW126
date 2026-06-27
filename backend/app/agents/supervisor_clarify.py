import json

from app.models.intent import ParsedIntent
from app.models.meal_plan import FillFieldsInput, SupervisorInput, SupervisorOutput
from app.services.llm import structured_completion

SUPERVISOR_SYSTEM = """You are a friendly cooking assistant supervisor.
Given missing field metadata from a schema, ask ONE concise clarifying question.
Do not mention internal field names. Be natural and conversational."""

FILL_SYSTEM = """You merge a user's clarification answer into a partial cooking intent.
Update only the missing fields. Keep existing non-null values unchanged.
Return a complete ParsedIntent object with all fields."""


def clarify(payload: SupervisorInput) -> SupervisorOutput:
    meta_json = json.dumps(payload.field_metadata, indent=2)
    user_prompt = (
        f"Original request: {payload.user_intent}\n"
        f"Partial understanding: {payload.partial_intent.model_dump_json()}\n"
        f"Missing fields metadata:\n{meta_json}\n"
        "Ask one question to fill the most important missing information."
    )
    return structured_completion(SUPERVISOR_SYSTEM, user_prompt, SupervisorOutput)


def fill_missing_fields(payload: FillFieldsInput) -> ParsedIntent:
    user_prompt = (
        f"Original request: {payload.user_intent}\n"
        f"Partial intent: {payload.partial_intent.model_dump_json()}\n"
        f"Missing fields: {payload.missing_fields}\n"
        f"User answer: {payload.clarification_answer}\n"
        "Merge the answer into the intent."
    )
    return structured_completion(FILL_SYSTEM, user_prompt, ParsedIntent)
