from __future__ import annotations

from app.agent.graph import build_agent_graph
from app.agent.tools.culture import get_culture_hints
from app.agent.tools.risk import risk_radar

try:
    from mcp.server.fastmcp import FastMCP
except Exception:  # pragma: no cover
    FastMCP = None


def create_mcp_server():
    if FastMCP is None:
        raise RuntimeError("未安装 mcp 依赖，无法启动 MCP Server。")

    mcp = FastMCP("chaoyun-yunnao")
    graph = build_agent_graph()

    @mcp.tool()
    def plan_trip(request: dict) -> dict:
        result = graph.invoke({"request": request})
        return result["final_response"]

    @mcp.tool()
    def get_culture_hint(request: dict) -> list[str]:
        return get_culture_hints(request)

    @mcp.tool()
    def risk_check(signals: dict, request: dict) -> list[str]:
        return risk_radar(signals, request)

    return mcp


def run_mcp_stdio() -> None:
    server = create_mcp_server()
    server.run(transport="stdio")


if __name__ == "__main__":
    run_mcp_stdio()
