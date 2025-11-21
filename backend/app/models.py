from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import date, time


class BirthData(BaseModel):
    date: str = Field(..., description="Birth date in YYYY-MM-DD format")
    time: str = Field(..., description="Birth time in HH:MM format")
    latitude: float = Field(..., description="Birth place latitude")
    longitude: float = Field(..., description="Birth place longitude")
    timezone: str = Field(..., description="Timezone (e.g., Asia/Kolkata)")
    name: Optional[str] = Field(None, description="User's name")
    session_id: Optional[str] = None


class ChatRequest(BaseModel):
    session_id: str
    message: str
    context: Optional[str] = Field(None, description="Context: career, marriage, finance, general")


class ChatMessage(BaseModel):
    role: str
    content: str


class ChartResponse(BaseModel):
    session_id: str
    chart_data: Dict
    message: str