import pytest
from unittest.mock import patch, AsyncMock
from app.services.gemini_service import gemini_service

@pytest.mark.asyncio
@patch("app.services.gemini_service.model.generate_content")
@patch("app.services.gemini_service.get_redis_client")
async def test_interpret_text(mock_redis, mock_gen):
    # Mock Redis
    mock_redis.return_value.get = AsyncMock(return_value=None)
    mock_redis.return_value.setex = AsyncMock(return_value=None)

    # Mock Gemini
    mock_gen.return_value.text = "Interpreted task"

    result = await gemini_service.interpret_text("Do something")
    assert result == "Interpreted task"
