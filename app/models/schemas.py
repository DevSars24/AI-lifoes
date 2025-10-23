from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Shared base for timestamps
class TimestampedModel(BaseModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

# -------------------
# Speech Schemas
# -------------------
class AudioUploadRequest(BaseModel):
    file_path: str  # Local path or URL for upload

class TranscriptResponse(BaseModel):
    transcript_id: str
    text: str
    confidence: float
    duration: float

# -------------------
# Notes Schemas
# -------------------
class NoteCreate(BaseModel):
    title: str
    content: str
    tags: List[str] = []

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None

class NoteSummaryResponse(BaseModel):
    summary: str
    key_points: List[str]

# -------------------
# Tasks Schemas
# -------------------
class TaskCreate(BaseModel):
    description: str
    priority: str = "medium"

class TaskUpdate(BaseModel):
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None

class TaskResponse(BaseModel):
    task_id: str
    description: str
    status: str = "pending"

# -------------------
# Learning Schemas
# -------------------
class LearningSuggestionRequest(BaseModel):
    user_input: str

class LearningSuggestionResponse(BaseModel):
    suggestion: str
    resources: List[str]

# -------------------
# TTS Schemas
# -------------------
class TTSRequest(BaseModel):
    text: str
    voice: str = "en-US-Standard-A"  # Default Google voice

class TTSResponse(BaseModel):
    audio_url: str  # Signed URL or base64
