from fastapi import APIRouter, HTTPException
from app.services.gemini_service import gemini_service
from app.services.db_service import db_service
from app.models.schemas import TaskCreate, TaskResponse, TaskUpdate
from app.models.mongo_models import TaskDoc
from typing import List, Dict, Any
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.auth_utils import verify_token

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_token(token)
    return payload

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

# -----------------------
# Create a new task
# -----------------------
@router.post("/create", response_model=TaskResponse)
async def create_task(task: TaskCreate, user=Depends(get_current_user)):  # 👈 only logged-in users
    interpreted = await gemini_service.interpret_text(task.description, "Extract task from text")
    doc = TaskDoc(description=interpreted, priority=task.priority)
    task_id = await db_service.insert_task(doc)
    return TaskResponse(task_id=task_id, description=doc.description, status=doc.status)


# -----------------------
# Get all tasks
# -----------------------
@router.get("/", response_model=List[Dict[str, Any]])
async def get_tasks():
    tasks = await db_service.get_tasks()
    for task in tasks:
        task["_id"] = str(task["_id"])
    return tasks

# -----------------------
# Get task by ID
# -----------------------
@router.get("/{task_id}", response_model=Dict[str, Any])
async def get_task_by_id(task_id: str):
    task = await db_service.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task["_id"] = str(task["_id"])
    return task

# -----------------------
# Update task fields
# -----------------------
@router.patch("/{task_id}", response_model=Dict[str, str])
async def update_task(task_id: str, task_update: TaskUpdate):
    updated = await db_service.update_task(task_id, task_update.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task updated successfully"}

# -----------------------
# Update task status only
# -----------------------
@router.patch("/{task_id}/status")
async def update_task_status(task_id: str, status: str):
    updated = await db_service.update_task_status(task_id, status)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Status updated"}

# -----------------------
# Delete task
# -----------------------
@router.delete("/{task_id}", response_model=Dict[str, str])
async def delete_task(task_id: str):
    deleted = await db_service.delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}
