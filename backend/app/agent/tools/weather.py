from __future__ import annotations

import json
from app.agent.tools.mock_data import MOCK_WEATHER
from app.services.weather_mcp import weather_client


def get_weather_signal(destination: str, use_mock: bool = True) -> dict:
    if use_mock:
        return MOCK_WEATHER.get(
            destination,
            {"condition": "多云", "temperature": 25, "humidity": 72},
        )
    
    # Use real MCP client
    try:
        result = weather_client.get_weather(destination)
        
        # Try to parse if the condition is a JSON string (common in tool outputs)
        condition_text = result.get("condition", "")
        if isinstance(condition_text, str) and condition_text.strip().startswith("{"):
            try:
                parsed = json.loads(condition_text)
                # If parsed successfully, we can extract fields or just return the parsed dict
                # merged with our structure.
                # For now, let's keep the raw text as 'condition' but also add parsed fields if simple.
                if isinstance(parsed, dict):
                    # If the tool returns a dict with 'weather' or similar, we might want to extract it.
                    # But let's trust the LLM to read the raw JSON string in 'condition'.
                    pass
            except json.JSONDecodeError:
                pass
                
        return result
    except Exception:
        # Fallback to a safe default if real call fails completely
        return {"condition": "获取失败", "temperature": 0, "humidity": 0}
