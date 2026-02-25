from __future__ import annotations

from app.agent.tools.mock_data import CHAOSHAN_CULTURE_RULES


def get_culture_hints(request: dict) -> list[str]:
    days = request.get("days", 2)
    style = request.get("travel_style", "轻松")
    companions = request.get("companions", [])
    
    hints = list(CHAOSHAN_CULTURE_RULES)
    
    if style in {"紧凑", "特种兵"}:
        hints.append("高强度行程建议保留午后缓冲段，避免连续跨城。")
    if days >= 3:
        hints.append("多日行程建议按城市分区游玩，减少折返。")
        
    # Companion-specific hints
    has_elderly = any(c.get("ageGroup") in ["老年 (60+)", "中年 (36-60)"] for c in companions)
    has_children = any(c.get("ageGroup") in ["儿童 (0-12)"] for c in companions)
    
    if has_elderly:
        hints.append("同行有长辈，建议安排功夫茶体验与平缓景点，避免过多台阶。")
    if has_children:
        hints.append("同行有儿童，推荐加入非遗手作体验（如剪纸、手拉壶）增加趣味性。")
        
    return hints
