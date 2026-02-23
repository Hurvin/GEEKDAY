from __future__ import annotations

from app.services.memory_service import (
    append_mid_term_if_confirmed,
    get_long_term_context,
    get_mid_term_memory,
    get_short_term_memory,
    update_user_profile,
)
from app.services.llm_client import LLMClient

llm_client = LLMClient()


def prepare_context_node(state: dict) -> dict:
    request = state.get("request", {})
    user_id = str(request.get("user_id") or "default")
    history = request.get("history", [])
    user_profile = request.get("user_profile", {})

    if isinstance(user_profile, dict) and user_profile:
        update_user_profile(user_id, user_profile)

    short_term = get_short_term_memory(history if isinstance(history, list) else [], max_rounds=3)
    mid_term = get_mid_term_memory(user_id, limit=8)
    long_term = get_long_term_context(user_id)
    return {
        "short_term_memory": short_term,
        "mid_term_memory": mid_term,
        "long_term_memory": long_term,
    }


def generate_chat_reply_node(state: dict) -> dict:
    request = state.get("request", {})
    request["short_term_memory"] = state.get("short_term_memory", [])
    request["mid_term_memory"] = state.get("mid_term_memory", [])
    request["long_term_memory"] = state.get("long_term_memory", {})
    return {"chat_response": llm_client.generate_chat_reply(request)}


def persist_context_node(state: dict) -> dict:
    request = state.get("request", {})
    user_id = str(request.get("user_id") or "default")
    user_message = str(request.get("message") or "")
    assistant_reply = str(state.get("chat_response", {}).get("reply") or "")
    append_mid_term_if_confirmed(
        user_id=user_id,
        user_message=user_message,
        assistant_reply=assistant_reply,
    )
    return {}
