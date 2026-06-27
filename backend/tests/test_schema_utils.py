from app.models.intent import MealSlot, ParsedIntent
from app.services.schema_utils import get_field_metadata, get_missing_fields


def test_missing_servings() -> None:
    intent = ParsedIntent(
        meal_slots=[MealSlot.DINNER],
        servings=None,
        cuisine_theme="North Indian",
        diet="vegetarian",
    )
    missing = get_missing_fields(intent, 30.0)
    assert missing == ["servings"]


def test_missing_meal_slots() -> None:
    intent = ParsedIntent(meal_slots=None, servings=4)
    missing = get_missing_fields(intent, 30.0)
    assert missing == ["meal_slots"]


def test_complete_intent() -> None:
    intent = ParsedIntent(meal_slots=[MealSlot.DINNER], servings=4)
    missing = get_missing_fields(intent, 30.0)
    assert missing == []


def test_field_metadata_from_schema() -> None:
    meta = get_field_metadata(ParsedIntent, ["servings"])
    assert len(meta) == 1
    assert meta[0].name == "servings"
    assert "people" in meta[0].description.lower()
