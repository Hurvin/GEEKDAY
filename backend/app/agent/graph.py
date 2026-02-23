from __future__ import annotations

from langgraph.graph import END, StateGraph

from app.agent.nodes import (
    apply_culture_rules_node,
    collect_signals_node,
    generate_itinerary_node,
    risk_refine_node,
)
from app.agent.state import PlannerState


def build_agent_graph():
    graph = StateGraph(PlannerState)
    graph.add_node("collectSignalsNode", collect_signals_node)
    graph.add_node("applyCultureRulesNode", apply_culture_rules_node)
    graph.add_node("generateItineraryNode", generate_itinerary_node)
    graph.add_node("riskRefineNode", risk_refine_node)

    graph.set_entry_point("collectSignalsNode")
    graph.add_edge("collectSignalsNode", "applyCultureRulesNode")
    graph.add_edge("applyCultureRulesNode", "generateItineraryNode")
    graph.add_edge("generateItineraryNode", "riskRefineNode")
    graph.add_edge("riskRefineNode", END)
    return graph.compile()
