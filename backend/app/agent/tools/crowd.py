from __future__ import annotations

from app.agent.tools.mock_data import MOCK_CROWD


def get_crowd_signal(destination: str, use_mock: bool = True) -> dict:
    if use_mock:
        # MVP 阶段先以固定热点样本模拟人流趋势
        return {
            "destination": destination,
            "hotspots": MOCK_CROWD,
            "summary": "核心城区热点偏拥挤，外围点位较舒适",
        }
    return {
        "destination": destination,
        "hotspots": {},
        "summary": "暂无实时人流数据",
    }
