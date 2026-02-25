from typing import List, Literal

from pydantic import BaseModel, Field


class PlanRequest(BaseModel):
    destination: str = Field(..., description="目的地，例如汕头/潮州/揭阳")
    days: int = Field(default=2, ge=1, le=7)
    travel_style: str = Field(default="轻松")
    travelers: str = Field(default="朋友")
    preferences: List[str] = Field(default_factory=list)
    constraints: List[str] = Field(default_factory=list)
    budget_level: str = Field(default="中等")
    model: str | None = Field(default=None, description="可选模型ID，留空则使用默认模型")


class ItineraryItem(BaseModel):
    day: int
    period: str
    activity: str
    reason: str


class PlanResponse(BaseModel):
    summary: str
    itinerary: List[ItineraryItem]
    culture_tips: List[str]
    risk_alerts: List[str]
    signal_basis: List[str]


class ModelOption(BaseModel):
    value: str
    label: str
    desc: str


class ChatMessage(BaseModel):
    role: str = Field(..., description="system/user/assistant")
    content: str


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="用户当前输入")
    history: List[ChatMessage] = Field(default_factory=list, description="历史对话")
    model: str | None = Field(default=None, description="可选模型ID")
    user_id: str = Field(default="default", description="用户唯一标识")
    user_profile: dict = Field(default_factory=dict, description="用户画像信息")


class ChatResponse(BaseModel):
    reply: str
    model_used: str


class FakeEventCreate(BaseModel):
    event_type: Literal["weather", "crowd"] = Field(..., description="事件类型")
    destination: str = Field(default="", description="目的地")
    day_index: int = Field(default=1, ge=1, description="第几天")
    old_value: str = Field(default="", description="变化前值")
    new_value: str = Field(default="", description="变化后值")
    note: str = Field(default="", description="补充说明")


class FakeEvent(FakeEventCreate):
    id: str
    created_at: int


class FakeEventConsumeResponse(BaseModel):
    events: List[FakeEvent] = Field(default_factory=list)


class McpServiceItem(BaseModel):
    name: str
    description: str
