from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=2, description="Business query from dashboard chatbot")


class ChartDataset(BaseModel):
    label: str
    data: List[Any]


class ChartPayload(BaseModel):
    type: str
    title: str
    labels: List[str]
    datasets: List[ChartDataset]
    xAxis: Optional[str] = None
    yAxis: Optional[str] = None
    meta: Dict[str, Any] = Field(default_factory=dict)


class InsightPayload(BaseModel):
    insight: str
    cause: str
    recommendation: str
    impact: str
    confidence: float


class ChatResponse(BaseModel):
    response_type: str
    intent: str
    chart: Optional[ChartPayload] = None
    analysis: InsightPayload
    answer: str
