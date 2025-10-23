from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.auth_utils import verify_token
from app.services.db_service import db_service
from app.models.schemas import NoteCreate, NoteUpdate
from app.models.mongo_models import NoteDoc
from pydantic import BaseModel
from typing import List, Dict, Any
from bson import ObjectId

# -----------------------
# JWT Authentication Setup
# -----------------------
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_token(token)
    return payload


# -----------------------
# Router Setup (all routes protected)
# -----------------------
router = APIRouter(
    prefix="/api/notes",
    tags=["notes"],
    dependencies=[Depends(get_current_user)]  # 👈 applies JWT check to every route
)


# -----------------------
# Response Schema
# -----------------------
class NoteListResponse(BaseModel):
    notes: List[Dict[str, Any]]


# -----------------------
# Get all notes
# -----------------------
@router.get("/", response_model=NoteListResponse)
async def get_notes():
    notes = await db_service.get_notes()
    for note in notes:
        note["_id"] = str(note["_id"])
    return {"notes": notes}


# -----------------------
# Create a new note
# -----------------------
@router.post("/", response_model=Dict[str, str])
async def create_note(note: NoteCreate):
    note_doc = NoteDoc(**note.dict())
    note_id = await db_service.insert_note(note_doc)
    return {"note_id": note_id}


# -----------------------
# Get note by ID
# -----------------------
@router.get("/{note_id}", response_model=Dict[str, Any])
async def get_note_by_id(note_id: str):
    note = await db_service.get_note_by_id(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    note["_id"] = str(note["_id"])
    return note


# -----------------------
# Update note by ID
# -----------------------
@router.patch("/{note_id}", response_model=Dict[str, str])
async def update_note(note_id: str, note: NoteUpdate):
    existing_note = await db_service.get_note_by_id(note_id)
    if not existing_note:
        raise HTTPException(status_code=404, detail="Note not found")

    updated_fields = note.dict(exclude_unset=True)
    await db_service.update_note(note_id, updated_fields)
    return {"message": "Note updated successfully"}


# -----------------------
# Delete note by ID
# -----------------------
@router.delete("/{note_id}", response_model=Dict[str, str])
async def delete_note(note_id: str):
    deleted = await db_service.delete_note(note_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": "Note deleted successfully"}
