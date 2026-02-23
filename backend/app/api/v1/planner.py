from fastapi import APIRouter

from app.agent.chat_graph import build_chat_graph
from app.agent.graph import build_agent_graph
from app.schemas.planner import ChatRequest, ChatResponse, ModelOption, PlanRequest, PlanResponse
from app.services.llm_client import LLMClient

router = APIRouter()
_graph = build_agent_graph()
_chat_graph = build_chat_graph()


@router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


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
