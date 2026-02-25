from __future__ import annotations

from app.agent.tools.mock_data import CHAOSHAN_CULTURE_RULES


def get_culture_hints(request: dict) -> list[str]:
    days = request.get("days", 2)
    style = request.get("travel_style", "轻松")
    hints = list(CHAOSHAN_CULTURE_RULES)
    if style in {"紧凑", "特种兵"}:
        hints.append("高强度行程建议保留午后缓冲段，避免连续跨城。")
    if days >= 3:
        hints.append("多日行程建议按城市分区游玩，减少折返。")
    return hints
