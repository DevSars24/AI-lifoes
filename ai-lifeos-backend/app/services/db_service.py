import motor.motor_asyncio
from bson import ObjectId
from typing import List, Dict, Any
from app.db.database import notes_collection, tasks_collection, transcripts_collection
from app.models.mongo_models import TranscriptDoc, NoteDoc, TaskDoc
from loguru import logger
from datetime import datetime

class DBService:

    # -------------------
    # Transcripts
    # -------------------
    @staticmethod
    async def insert_transcript(transcript: TranscriptDoc) -> str:
        try:
            doc = transcript.dict()
            result = await transcripts_collection.insert_one(doc)
            logger.info(f"Inserted transcript: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Failed to insert transcript: {e}")
            raise RuntimeError("Database error: cannot insert transcript")

    # -------------------
    # Notes CRUD
    # -------------------
    @staticmethod
    async def insert_note(note: NoteDoc) -> str:
        try:
            doc = note.dict()
            doc["created_at"] = datetime.utcnow()
            result = await notes_collection.insert_one(doc)
            logger.info(f"Inserted note: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Failed to insert note: {e}")
            raise RuntimeError("Database error: cannot insert note")

    @staticmethod
    async def get_notes() -> List[Dict[str, Any]]:
        try:
            cursor = notes_collection.find()
            notes = await cursor.to_list(length=100)
            for note in notes:
                note["_id"] = str(note["_id"])
            return notes
        except Exception as e:
            logger.error(f"Failed to fetch notes: {e}")
            return []

    @staticmethod
    async def get_note_by_id(note_id: str) -> Dict[str, Any]:
        try:
            note = await notes_collection.find_one({"_id": ObjectId(note_id)})
            if note:
                note["_id"] = str(note["_id"])
            return note
        except Exception as e:
            logger.error(f"Failed to fetch note {note_id}: {e}")
            return None

    @staticmethod
    async def update_note(note_id: str, fields: Dict[str, Any]) -> bool:
        try:
            fields["updated_at"] = datetime.utcnow()
            result = await notes_collection.update_one(
                {"_id": ObjectId(note_id)},
                {"$set": fields}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Failed to update note {note_id}: {e}")
            return False

    @staticmethod
    async def delete_note(note_id: str) -> bool:
        try:
            result = await notes_collection.delete_one({"_id": ObjectId(note_id)})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Failed to delete note {note_id}: {e}")
            return False

    # -------------------
    # Tasks CRUD
    # -------------------
    @staticmethod
    async def insert_task(task: TaskDoc) -> str:
        try:
            doc = task.dict()
            doc["created_at"] = datetime.utcnow()
            result = await tasks_collection.insert_one(doc)
            logger.info(f"Inserted task: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Failed to insert task: {e}")
            raise RuntimeError("Database error: cannot insert task")

    @staticmethod
    async def get_tasks() -> List[Dict[str, Any]]:
        try:
            cursor = tasks_collection.find()
            tasks = await cursor.to_list(length=100)
            for task in tasks:
                task["_id"] = str(task["_id"])
            return tasks
        except Exception as e:
            logger.error(f"Failed to fetch tasks: {e}")
            return []

    @staticmethod
    async def get_task_by_id(task_id: str) -> Dict[str, Any]:
        try:
            task = await tasks_collection.find_one({"_id": ObjectId(task_id)})
            if task:
                task["_id"] = str(task["_id"])
            return task
        except Exception as e:
            logger.error(f"Failed to fetch task {task_id}: {e}")
            return None

    @staticmethod
    async def update_task(task_id: str, fields: Dict[str, Any]) -> bool:
        try:
            fields["updated_at"] = datetime.utcnow()
            result = await tasks_collection.update_one(
                {"_id": ObjectId(task_id)},
                {"$set": fields}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Failed to update task {task_id}: {e}")
            return False

    @staticmethod
    async def update_task_status(task_id: str, status: str) -> bool:
        return await DBService.update_task(task_id, {"status": status})

    @staticmethod
    async def delete_task(task_id: str) -> bool:
        try:
            result = await tasks_collection.delete_one({"_id": ObjectId(task_id)})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Failed to delete task {task_id}: {e}")
            return False

# -------------------
# Instantiate service
# -------------------
db_service = DBService()
