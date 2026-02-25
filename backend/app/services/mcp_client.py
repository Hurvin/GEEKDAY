from __future__ import annotations

import logging
from typing import Any

import httpx

logger = logging.getLogger(__name__)

MCP_SERVER_URL = "https://mcp.api-inference.modelscope.net/97cb26640caa41/mcp"


class McpClient:
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

    def call_tool(self, tool_name: str, arguments: dict) -> dict[str, Any]:
        if not self.session_id:
            try:
                self.initialize()
            except Exception as e:
                return {"error": f"MCP Init Failed: {e}"}

        logger.info(f"Calling tool: {tool_name} with args: {arguments}")
        payload = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {"name": tool_name, "arguments": arguments},
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
            return data
        except Exception as e:
            logger.error(f"Tool call failed: {e}")
            return {"error": str(e)}

    def get_weather(self, city: str) -> dict[str, Any]:
        data = self.call_tool("maps_weather", {"city": city})
        if "result" in data and "content" in data["result"]:
            content_list = data["result"]["content"]
            if content_list and content_list[0].get("type") == "text":
                return {
                    "condition": content_list[0].get("text"),
                    "temperature": 0,
                    "humidity": 0,
                    "raw": data
                }
        return {"condition": "未知", "temperature": 0, "humidity": 0, "raw": data}

    def search_poi(self, keywords: str, city: str = "潮州") -> list[dict]:
        """Search for POIs (Point of Interest)"""
        data = self.call_tool("maps_text_search", {"keywords": keywords, "city": city})
        # Parse logic can be added here based on actual response structure
        return data

    def search_nearby(self, location: str, keywords: str) -> list[dict]:
        """Search for nearby places"""
        data = self.call_tool("maps_around_search", {"location": location, "keywords": keywords})
        return data

    def get_travel_distance(self, origin: str, destination: str, mode: str = "driving") -> dict:
        """Get distance and duration between two points"""
        tool_map = {
            "driving": "maps_direction_driving",
            "walking": "maps_direction_walking",
            "bicycling": "maps_bicycling",
            "transit": "maps_direction_transit_integrated"
        }
        tool_name = tool_map.get(mode, "maps_direction_driving")
        
        args = {"origin": origin, "destination": destination}
        if mode == "transit":
            args.update({"city": "潮州", "cityd": "潮州"}) # Default city
            
        data = self.call_tool(tool_name, args)
        return data


# Singleton instance
mcp_client = McpClient()
