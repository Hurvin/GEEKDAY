from fastapi import APIRouter

from app.agent.graph import build_agent_graph
from app.schemas.planner import ModelOption, PlanRequest, PlanResponse
from app.services.llm_client import LLMClient

router = APIRouter()
_graph = build_agent_graph()


@router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/plan", response_model=PlanResponse)
def plan_trip(payload: PlanRequest) -> PlanResponse:
    result = _graph.invoke({"request": payload.model_dump()})
    return PlanResponse(**result["final_response"])


@router.get("/models", response_model=list[ModelOption])
def list_models() -> list[ModelOption]:
    return [ModelOption(**item) for item in LLMClient.get_model_catalog()]
