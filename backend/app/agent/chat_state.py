from typing import Any, TypedDict


class ChatState(TypedDict, total=False):
    request: dict[str, Any]
    short_term_memory: list[dict[str, str]]
    mid_term_memory: list[dict[str, Any]]
    long_term_memory: dict[str, Any]
    chat_response: dict[str, str]
