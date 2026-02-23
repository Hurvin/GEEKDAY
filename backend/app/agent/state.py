from typing import Any, TypedDict


class PlannerState(TypedDict, total=False):
    request: dict[str, Any]
    signals: dict[str, Any]
    culture_hints: list[str]
    draft_plan: dict[str, Any]
    final_response: dict[str, Any]
