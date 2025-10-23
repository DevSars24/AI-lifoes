from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
from loguru import logger
from starlette.exceptions import HTTPException as StarletteHTTPException

# Internal Imports
from app.db.database import close_db_connection
from app.core.logger import app_logger
from app.core.exception_handler import (
    http_exception_handler,
    global_exception_handler
)

# Routers
from app.routers import notes, tasks, speech, learning, auth  # 👈 Added auth router

# ---------------------------
# Lifespan Manager
# ---------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    app_logger.info("🚀 Starting up AI LifeOS Backend...")
    yield
    await close_db_connection()
    app_logger.info("🛑 Shutting down AI LifeOS Backend...")

# ---------------------------
# FastAPI App Setup
# ---------------------------
app = FastAPI(
    title="AI LifeOS Backend",
    version="1.0.0",
    lifespan=lifespan,
)

# ---------------------------
# Middleware
# ---------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# Exception Handlers
# ---------------------------
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

# ---------------------------
# Routers
# ---------------------------
app.include_router(auth.router)       # 👈 New Authentication router
app.include_router(notes.router)
app.include_router(tasks.router)
app.include_router(speech.router)
app.include_router(learning.router)

# ---------------------------
# Root Route
# ---------------------------
@app.get("/")
async def root():
    return {"message": "AI LifeOS Backend is running ✅"}

# ---------------------------
# Entry Point
# ---------------------------
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
