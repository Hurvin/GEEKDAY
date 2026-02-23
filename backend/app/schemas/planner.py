from typing import List

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
