from __future__ import annotations

import logging
from typing import Any

import httpx

logger = logging.getLogger(__name__)

MCP_SERVER_URL = "https://mcp.api-inference.modelscope.net/97cb26640caa41/mcp"


class WeatherMcpClient:
    def __init__(self) -> None:
        self.session_id: str | None = None
        self.client = httpx.Client(timeout=30.0)

    def initialize(self) -> None:
        logger.info("Initializing MCP connection...")
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "roots": {"listChanged": True},
                    "sampling": {},
                },
                "clientInfo": {"name": "geek-client", "version": "0.1"},
            },
        }
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        }

        try:
            response = self.client.post(MCP_SERVER_URL, json=payload, headers=headers)
            response.raise_for_status()

            # Case-insensitive header lookup
            for key, value in response.headers.items():
                if key.lower() == "mcp-session-id":
                    self.session_id = value
                    logger.info(f"Initialized successfully, Session ID: {self.session_id}")
                    self.send_initialized_notification()
                    return

            logger.warning("Warning: Mcp-Session-Id header not found in initialization response")

        except Exception as e:
            logger.error(f"Initialization failed: {e}")
            # Reset session_id on failure to allow retry
            self.session_id = None
            raise

    def send_initialized_notification(self) -> None:
        logger.info("Sending notifications/initialized...")
        payload = {"jsonrpc": "2.0", "method": "notifications/initialized"}
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "Mcp-Session-Id": self.session_id or "",
        }
        try:
            self.client.post(MCP_SERVER_URL, json=payload, headers=headers)
            logger.info("Notification sent")
        except Exception as e:
            logger.error(f"Failed to send notification: {e}")

    def get_weather(self, city: str) -> dict[str, Any]:
        if not self.session_id:
            try:
                self.initialize()
            except Exception as e:
                return {
                    "condition": "未知",
                    "temperature": 0,
                    "humidity": 0,
                    "error": f"MCP Init Failed: {e}",
                }

        logger.info(f"Querying weather for {city}...")
        payload = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {"name": "maps_weather", "arguments": {"city": city}},
        }
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "Mcp-Session-Id": self.session_id or "",
        }

        try:
            response = self.client.post(MCP_SERVER_URL, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()

            # Process MCP response
            # Expected structure: {"jsonrpc": "2.0", "id": 2, "result": {"content": [{"type": "text", "text": "..."}]}}
            if "result" in data and "content" in data["result"]:
                content_list = data["result"]["content"]
                if content_list and content_list[0].get("type") == "text":
                    text_result = content_list[0].get("text")
                    # Here we return the raw text as 'condition' for the LLM to process,
                    # or we could try to parse it if it's JSON.
                    # Since the downstream node uses it in a prompt, returning the text is fine.
                    return {
                        "condition": text_result,  # Put full text in condition so LLM sees it
                        "temperature": 0, # Placeholder
                        "humidity": 0,    # Placeholder
                        "raw": data
                    }

            return {
                "condition": "未知",
                "temperature": 0,
                "humidity": 0,
                "raw": data
            }

        except Exception as e:
            logger.error(f"Weather query failed: {e}")
            # If session is invalid, maybe we should clear it?
            # For now, just return error.
            return {
                "condition": "未知",
                "temperature": 0,
                "humidity": 0,
                "error": str(e),
            }


# Singleton instance
weather_client = WeatherMcpClient()
