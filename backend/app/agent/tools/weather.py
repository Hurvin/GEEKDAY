from __future__ import annotations

from app.agent.tools.mock_data import MOCK_WEATHER


def get_weather_signal(destination: str, use_mock: bool = True) -> dict:
    if use_mock:
        return MOCK_WEATHER.get(
            destination,
            {"condition": "多云", "temperature": 25, "humidity": 72},
        )
    return {"condition": "未知", "temperature": 25, "humidity": 70}
