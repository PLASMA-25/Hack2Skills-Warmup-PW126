from typing import Literal

from app.models.intent import MealSlot, ParsedIntent
from app.models.meal_plan import (
    BudgetAgentInput,
    FillFieldsInput,
    GroceryAgentInput,
    IntentExtractInput,
    MealAgentInput,
    SubstitutionsAgentInput,
    SupervisorInput,
)
from app.agents.budget_agent import check_budget
from app.agents.grocery_agent import build_grocery_list
from app.agents.intent_extractor import extract_intent
from app.agents.meal_agents import plan_breakfast, plan_dinner, plan_lunch
from app.agents.substitutions_agent import suggest_substitutions
from app.agents.supervisor_clarify import clarify, fill_missing_fields
from app.graph.state import GraphState
from app.services.schema_utils import FieldMeta, get_field_metadata, get_missing_fields


def prepare_intent_node(state: GraphState) -> GraphState:
    if state.get("clarification_answer") and state.get("partial_intent"):
        filled = fill_missing_fields(
            FillFieldsInput(
                partial_intent=state["partial_intent"],
                clarification_answer=state["clarification_answer"],
                missing_fields=state.get("missing_fields", []),
                user_intent=state["user_intent"],
            )
        )
        return {**state, "parsed_intent": filled, "status": "planning"}
    extracted = extract_intent(
        IntentExtractInput(
            user_intent=state["user_intent"],
            budget=state["budget"],
            currency=state["currency"],
        )
    )
    return {**state, "parsed_intent": extracted, "status": "planning"}


def validate_intent_node(state: GraphState) -> GraphState:
    intent = state.get("parsed_intent")
    if intent is None:
        return {**state, "missing_fields": ["meal_slots", "servings"], "status": "needs_clarification"}
    missing = get_missing_fields(intent, state.get("budget"))
    return {**state, "missing_fields": missing}


def supervisor_clarify_node(state: GraphState) -> GraphState:
    intent = state.get("parsed_intent")
    if intent is None:
        return {**state, "status": "needs_clarification", "clarification_question": "What would you like to cook?"}
    missing = state.get("missing_fields", [])
    meta = get_field_metadata(ParsedIntent, missing)
    result = clarify(
        SupervisorInput(
            missing_fields=missing,
            field_metadata=[m.model_dump() for m in meta],
            partial_intent=intent,
            user_intent=state["user_intent"],
        )
    )
    return {
        **state,
        "clarification_question": result.question,
        "partial_intent": intent,
        "status": "needs_clarification",
    }


def init_meal_queue_node(state: GraphState) -> GraphState:
    intent = state["parsed_intent"]
    slots = list(intent.meal_slots or [])
    return {
        **state,
        "pending_meal_slots": slots,
        "meals": state.get("meals") or {},
        "retries": state.get("retries", 0),
    }


def plan_next_meal_node(state: GraphState) -> GraphState:
    pending = list(state.get("pending_meal_slots") or [])
    if not pending:
        return state
    slot = pending[0]
    rest = pending[1:]
    intent = state["parsed_intent"]
    agent_input = MealAgentInput(
        slot=slot,
        intent=intent,
        budget=state["budget"],
        currency=state["currency"],
        reduce_cost=state.get("reduce_cost", False),
    )
    if slot == MealSlot.BREAKFAST:
        output = plan_breakfast(agent_input)
    elif slot == MealSlot.LUNCH:
        output = plan_lunch(agent_input)
    else:
        output = plan_dinner(agent_input)
    meals = dict(state.get("meals") or {})
    meals[slot.value] = output.meal
    return {**state, "pending_meal_slots": rest, "meals": meals}


def grocery_node(state: GraphState) -> GraphState:
    intent = state["parsed_intent"]
    output = build_grocery_list(
        GroceryAgentInput(
            meals=state.get("meals") or {},
            servings=intent.servings or 1,
            currency=state["currency"],
        )
    )
    return {**state, "grocery_list": output.items}


def substitutions_node(state: GraphState) -> GraphState:
    output = suggest_substitutions(
        SubstitutionsAgentInput(
            grocery_list=state.get("grocery_list") or [],
            intent=state["parsed_intent"],
            budget=state["budget"],
            currency=state["currency"],
        )
    )
    return {**state, "substitutions": output.substitutions}


def budget_node(state: GraphState) -> GraphState:
    output = check_budget(
        BudgetAgentInput(
            grocery_list=state.get("grocery_list") or [],
            budget=state["budget"],
            currency=state["currency"],
        )
    )
    return {**state, "budget_result": output.result}


def finalize_node(state: GraphState) -> GraphState:
    return {**state, "status": "complete"}


def retry_budget_node(state: GraphState) -> GraphState:
    intent = state["parsed_intent"]
    slots = list(intent.meal_slots or [])
    return {
        **state,
        "pending_meal_slots": slots,
        "meals": {},
        "grocery_list": [],
        "substitutions": [],
        "budget_result": None,
        "reduce_cost": True,
        "retries": state.get("retries", 0) + 1,
    }
