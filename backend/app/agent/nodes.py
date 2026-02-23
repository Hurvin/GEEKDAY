from __future__ import annotations

from app.agent.tools.crowd import get_crowd_signal
from app.agent.tools.culture import get_culture_hints
from app.agent.tools.risk import risk_radar
from app.agent.tools.weather import get_weather_signal
from app.core.config import settings
from app.services.llm_client import LLMClient

llm_client = LLMClient()


def collect_signals_node(state: dict) -> dict:
    request = state["request"]
    destination = request.get("destination", "汕头")
    weather = get_weather_signal(destination, use_mock=settings.use_mock_data)
    crowd = get_crowd_signal(destination, use_mock=settings.use_mock_data)
    return {"signals": {"weather": weather, "crowd": crowd}}


def apply_culture_rules_node(state: dict) -> dict:
    hints = get_culture_hints(state["request"])
    return {"culture_hints": hints}


def generate_itinerary_node(state: dict) -> dict:
    prompt_data = {
        "request": state["request"],
        "signals": state.get("signals", {}),
        "culture_hints": state.get("culture_hints", []),
        "risk_alerts": state.get("risk_alerts", []),
        "signal_basis": [
            f"天气：{state.get('signals', {}).get('weather', {}).get('condition', '未知')}",
            state.get("signals", {}).get("crowd", {}).get("summary", "暂无人流摘要"),
        ],
    }
    draft = llm_client.generate_itinerary(prompt_data)
    return {"draft_plan": draft}


def risk_refine_node(state: dict) -> dict:
    alerts = risk_radar(state.get("signals", {}), state.get("request", {}))
    draft = state.get("draft_plan", {})
    final_response = {
        "summary": draft.get("summary", "已生成行程建议"),
        "itinerary": draft.get("itinerary", []),
        "culture_tips": draft.get("culture_tips", state.get("culture_hints", [])),
        "risk_alerts": list(dict.fromkeys(draft.get("risk_alerts", []) + alerts)),
        "signal_basis": draft.get("signal_basis", []),
    }
    return {"risk_alerts": alerts, "final_response": final_response}
