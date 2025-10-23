import httpx
from loguru import logger
from typing import Any, Dict, Optional
import redis.asyncio as redis
from app.core.config import config


# ---------------------------
# Redis Client
# ---------------------------
async def get_redis_client() -> redis.Redis:
    """Initialize and return an async Redis client."""
    return redis.from_url(config.REDIS_URL, decode_responses=True)


# ---------------------------
# Generic External API Caller
# ---------------------------
async def call_external_api(
    url: str,
    method: str = "GET",
    json_data: Optional[Dict] = None,
    headers: Optional[Dict] = None,
) -> Dict[str, Any]:
    """Make async HTTP requests with error handling."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method, url, json=json_data, headers=headers, timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            logger.error(f"API call failed: {e}")
            raise ValueError(f"External API error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error in API call: {e}")
            raise


# ---------------------------
# Cache Helper
# ---------------------------
async def cache_result(
    redis_client: redis.Redis, key: str, value: str, ttl: int = 3600
) -> None:
    """Cache a result with TTL."""
    await redis_client.setex(key, ttl, value)
