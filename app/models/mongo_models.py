from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# MongoDB document models (for validation on insert/update)
class TranscriptDoc(BaseModel):
    transcript_id: str
    text: str
    confidence: float
    duration: float
    user_id: Optional[str] = None  # For multi-user scalability


class NoteDoc(BaseModel):
    title: str
    content: str
    summary: Optional[str] = None
    tags: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)  # optional but useful


class TaskDoc(BaseModel):
    description: str
    priority: str
    status: str = "pending"
    created_at: datetime = Field(default_factory=datetime.utcnow)
