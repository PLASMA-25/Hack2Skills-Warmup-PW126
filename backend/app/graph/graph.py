from langgraph.graph import END, StateGraph

from app.graph import nodes, routing
from app.graph.state import GraphState


def build_meal_planner_graph():
    graph = StateGraph(GraphState)

    graph.add_node("prepare_intent", nodes.prepare_intent_node)
    graph.add_node("validate_intent", nodes.validate_intent_node)
    graph.add_node("supervisor_clarify", nodes.supervisor_clarify_node)
    graph.add_node("init_meal_queue", nodes.init_meal_queue_node)
    graph.add_node("plan_next_meal", nodes.plan_next_meal_node)
    graph.add_node("grocery", nodes.grocery_node)
    graph.add_node("substitutions", nodes.substitutions_node)
    graph.add_node("budget", nodes.budget_node)
    graph.add_node("retry_budget", nodes.retry_budget_node)
    graph.add_node("finalize", nodes.finalize_node)

    graph.set_entry_point("prepare_intent")
    graph.add_edge("prepare_intent", "validate_intent")
    graph.add_conditional_edges(
        "validate_intent",
        routing.route_after_validate,
        {
            "supervisor_clarify": "supervisor_clarify",
            "init_meal_queue": "init_meal_queue",
        },
    )
    graph.add_edge("supervisor_clarify", END)
    graph.add_edge("init_meal_queue", "plan_next_meal")
    graph.add_conditional_edges(
        "plan_next_meal",
        routing.route_after_meal,
        {
            "plan_next_meal": "plan_next_meal",
            "grocery": "grocery",
        },
    )
    graph.add_edge("grocery", "substitutions")
    graph.add_edge("substitutions", "budget")
    graph.add_conditional_edges(
        "budget",
        routing.route_after_budget,
        {
            "retry_budget": "retry_budget",
            "finalize": "finalize",
        },
    )
    graph.add_edge("retry_budget", "plan_next_meal")
    graph.add_edge("finalize", END)

    return graph.compile()
