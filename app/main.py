from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
from loguru import logger
from app.routers import notes, tasks, speech, learning  # Imports

# Import your routers (uncomment/add all)
from app.routers import notes, tasks, speech, learning  # Now including speech & learning
from app.db.database import close_db_connection
from app.core.logger import app_logger  # Make sure this exists
from app.core.exception_handler import (
    http_exception_handler,
    global_exception_handler
)
from starlette.exceptions import HTTPException as StarletteHTTPException

# -------------------------------
# Lifespan manager
# -------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    app_logger.info("Starting up...")
    yield
    await close_db_connection()
    app_logger.info("Shutting down...")

# -------------------------------
# FastAPI app setup
# -------------------------------
app = FastAPI(
    title="AI LifeOS Backend",
    version="1.0.0",
    lifespan=lifespan
)

# -------------------------------
# CORS middleware
# -------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# Exception handlers
# -------------------------------
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

# -------------------------------
# Routers (Now all included!)


from app.routers import notes, tasks, speech, learning  # Imports

# Routers section
app.include_router(notes.router)
app.include_router(tasks.router)
app.include_router(speech.router)
app.include_router(learning.router)  # Yeh line uncommented ho

# -------------------------------
# Root endpoint
# -------------------------------
@app.get("/")
async def root():
    return {"message": "AI LifeOS Backend is running ✅"}

# -------------------------------
# Entry point
# -------------------------------
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)