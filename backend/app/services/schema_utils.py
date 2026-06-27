from pydantic import BaseModel
from pydantic.fields import FieldInfo

from app.models.intent import ParsedIntent


REQUIRED_INTENT_FIELDS = ["meal_slots", "servings"]


class FieldMeta(BaseModel):
    name: str
    description: str
    type_hint: str


def get_missing_fields(intent: ParsedIntent, budget: float | None) -> list[str]:
    missing: list[str] = []
    if budget is None or budget <= 0:
        missing.append("budget")
    if not intent.meal_slots:
        missing.append("meal_slots")
    if intent.servings is None:
        missing.append("servings")
    return missing


def get_field_metadata(model: type[BaseModel], field_names: list[str]) -> list[FieldMeta]:
    metadata: list[FieldMeta] = []
    for name in field_names:
        if name == "budget":
            metadata.append(
                FieldMeta(
                    name="budget",
                    description="Maximum budget for groceries",
                    type_hint="number",
                )
            )
            continue
        field_info: FieldInfo | None = model.model_fields.get(name)
        if field_info is None:
            continue
        description = field_info.description or name.replace("_", " ")
        annotation = field_info.annotation
        type_hint = str(annotation) if annotation is not None else "string"
        metadata.append(FieldMeta(name=name, description=description, type_hint=type_hint))
    return metadata
