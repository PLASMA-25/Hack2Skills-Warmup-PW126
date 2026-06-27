from fastapi import APIRouter, HTTPException

from app.graph.graph import build_meal_planner_graph
from app.graph.state import GraphState
from app.models.meal_plan import ClarificationPrompt, PlanRequest, PlanResponse, PlanResult

router = APIRouter(prefix="/api", tags=["plan"])

_graph = None


def get_graph():
    global _graph
    if _graph is None:
        _graph = build_meal_planner_graph()
    return _graph


@router.post("/plan", response_model=PlanResponse)
def create_plan(request: PlanRequest) -> PlanResponse:
    from app.config import settings

    if not settings.openai_api_key:
        raise HTTPException(
            status_code=503,
            detail="OPENAI_API_KEY is not configured. Add it to .env at the repo root.",
        )

    initial_state: GraphState = {
        "user_intent": request.user_intent,
        "budget": request.budget,
        "currency": request.currency,
        "partial_intent": request.partial_intent,
        "clarification_answer": request.clarification_answer,
        "missing_fields": [],
        "retries": 0,
        "reduce_cost": False,
    }
    if request.clarification_answer and request.partial_intent:
        from app.services.schema_utils import get_missing_fields

        initial_state["missing_fields"] = get_missing_fields(
            request.partial_intent, request.budget
        )

    try:
        result = get_graph().invoke(initial_state)
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Meal planning failed. Please try again.") from exc

    status = result.get("status", "complete")
    if status == "needs_clarification":
        partial = result.get("partial_intent") or result.get("parsed_intent")
        if partial is None:
            raise HTTPException(status_code=502, detail="Clarification required but intent missing")
        return PlanResponse(
            status="needs_clarification",
            clarification=ClarificationPrompt(
                question=result.get("clarification_question") or "Could you provide more details?",
                missing_fields=result.get("missing_fields") or [],
                partial_intent=partial,
            ),
        )

    parsed = result.get("parsed_intent")
    budget_result = result.get("budget_result")
    if parsed is None or budget_result is None:
        raise HTTPException(status_code=502, detail="Incomplete plan result")

    return PlanResponse(
        status="complete",
        plan=PlanResult(
            parsed_intent=parsed,
            meals=result.get("meals") or {},
            grocery_list=result.get("grocery_list") or [],
            substitutions=result.get("substitutions") or [],
            budget=budget_result,
            retries=result.get("retries", 0),
        ),
    )
