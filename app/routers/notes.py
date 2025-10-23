from fastapi import APIRouter, HTTPException
from app.services.db_service import db_service
from app.models.schemas import NoteCreate, NoteUpdate
from app.models.mongo_models import NoteDoc
from pydantic import BaseModel
from typing import List, Dict, Any
from bson import ObjectId

router = APIRouter(prefix="/api/notes", tags=["notes"])

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
    notes = await db_service.get_notes()
    for note in notes:
        if str(note["_id"]) == note_id:
            note["_id"] = str(note["_id"])
            return note
    raise HTTPException(status_code=404, detail="Note not found")

# -----------------------
# Update note by ID
# -----------------------
@router.patch("/{note_id}", response_model=Dict[str, str])
async def update_note(note_id: str, note: NoteUpdate):
    notes = await db_service.get_notes()
    for existing_note in notes:
        if str(existing_note["_id"]) == note_id:
            # Update fields if provided
            updated_note = existing_note.copy()
            if note.title is not None:
                updated_note["title"] = note.title
            if note.content is not None:
                updated_note["content"] = note.content
            if note.tags is not None:
                updated_note["tags"] = note.tags

            # Save updated note in DB
            await db_service.update_note(note_id, updated_note)
            return {"message": "Note updated successfully"}
    raise HTTPException(status_code=404, detail="Note not found")

# -----------------------
# Delete note by ID
# -----------------------
@router.delete("/{note_id}", response_model=Dict[str, str])
async def delete_note(note_id: str):
    deleted = await db_service.delete_note(note_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": "Note deleted successfully"}
