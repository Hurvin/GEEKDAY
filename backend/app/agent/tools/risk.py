from __future__ import annotations


def risk_radar(signals: dict, request: dict) -> list[str]:
    alerts: list[str] = []
    weather = signals.get("weather", {})
    crowd = signals.get("crowd", {})

    if weather.get("condition") in {"小雨", "暴雨", "雷阵雨"}:
        alerts.append("天气存在降雨，建议优先室内备选行程并携带雨具。")

    hotspots = crowd.get("hotspots", {})
    crowded = [k for k, v in hotspots.items() if v.get("level") == "high"]
    if crowded:
        alerts.append(f"以下区域可能拥堵：{', '.join(crowded)}，建议错峰或替代路线。")

    if "老人" in request.get("travelers", ""):
        alerts.append("同行含长辈，建议减少夜间跨区移动并提升休息频次。")
        
    companions = request.get("companions", [])
    for person in companions:
        name = person.get("name", "同行人员")
        health = person.get("healthCondition", "")
        if health:
            alerts.append(f"注意 {name} 的特殊情况：{health}，请提前确认相关设施。")
            
    return alerts
