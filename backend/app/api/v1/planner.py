from fastapi import APIRouter

from app.agent.chat_graph import build_chat_graph
from app.agent.graph import build_agent_graph
from app.agent.tools.weather import get_weather_signal
from app.schemas.planner import (
    ChatRequest,
    ChatResponse,
    FakeEventConsumeResponse,
    FakeEventCreate,
    FakeEvent,
    McpServiceItem,
    ModelOption,
    PlanRequest,
    PlanResponse,
)
from app.services.llm_client import LLMClient
from app.services.fake_events import fake_event_store

router = APIRouter()
_graph = build_agent_graph()
_chat_graph = build_chat_graph()


@router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/weather")
def get_weather(city: str, days: int = 1, test_mode: bool = False) -> dict:
    if test_mode:
        # Force change every minute for demo
        demo_conditions = ["晴朗", "多云", "小雨", "雷阵雨", "大风", "阴", "暴雨"]
        import time
        import random
        
        # Seed with time-based value to ensure consistency within the same minute/interval
        # but change across intervals.
        # Change every 60 seconds
        base_seed = int(time.time() / 60)
        random.seed(base_seed)
        
        forecast = []
        for i in range(days):
            # Generate a deterministic condition for this time slot + day offset
            # We add 'i' to seed so days are different
            day_seed = base_seed + i
            random.seed(day_seed)
            cond = random.choice(demo_conditions)
            forecast.append({
                "day": i + 1,
                "condition": cond,
                "temperature": random.randint(20, 30)
            })
            
        real_data = get_weather_signal(city, use_mock=False)
        real_data["forecast"] = forecast
        # Also update current condition to match Day 1
        if forecast:
            real_data["condition"] = forecast[0]["condition"]
            
        return real_data
        
    # Normal mode
    data = get_weather_signal(city, use_mock=False)
    # If real tool doesn't provide forecast, we might just return current
    # or let frontend handle it.
    # For consistency, let's ensure 'forecast' field exists even if empty or just current
    if "forecast" not in data:
        # Fallback: just use current condition for day 1 if we asked for days
        data["forecast"] = [{
            "day": 1, 
            "condition": data.get("condition", "未知"),
            "temperature": data.get("temperature", 0)
        }]
    return data


@router.post("/plan", response_model=PlanResponse)
def plan_trip(payload: PlanRequest) -> PlanResponse:
    result = _graph.invoke({"request": payload.model_dump()})
    return PlanResponse(**result["final_response"])


@router.post("/chat", response_model=ChatResponse)
def chat_with_agent(payload: ChatRequest) -> ChatResponse:
    result = _chat_graph.invoke({"request": payload.model_dump()})
    return ChatResponse(**result["chat_response"])


@router.get("/models", response_model=list[ModelOption])
def list_models() -> list[ModelOption]:
    return [ModelOption(**item) for item in LLMClient.get_model_catalog()]


@router.post("/fake/events", response_model=FakeEvent)
def create_fake_event(payload: FakeEventCreate) -> FakeEvent:
    return fake_event_store.push(payload)


@router.get("/fake/events/consume", response_model=FakeEventConsumeResponse)
def consume_fake_events(limit: int = 20) -> FakeEventConsumeResponse:
    return FakeEventConsumeResponse(events=fake_event_store.consume(limit=limit))


@router.get("/mcp/services", response_model=list[McpServiceItem])
def list_mcp_services() -> list[McpServiceItem]:
    return [
        McpServiceItem(name="maps_weather", description="询问天气"),
        McpServiceItem(name="maps_text_search", description="搜索地点"),
        McpServiceItem(name="maps_around_search", description="周边推荐"),
        McpServiceItem(name="maps_direction_driving", description="驾车导航"),
        McpServiceItem(name="maps_direction_walking", description="步行导航"),
        McpServiceItem(name="maps_bicycling", description="骑行导航"),
        McpServiceItem(name="maps_direction_transit_integrated", description="公交地铁"),
    ]
