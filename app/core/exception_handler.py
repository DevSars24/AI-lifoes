from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from loguru import logger

async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP Error: {exc.detail} | Path: {request.url}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

async def global_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unexpected Error: {exc} | Path: {request.url}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error. Please try again later."}
    )
