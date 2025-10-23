import pytest
from unittest.mock import AsyncMock, patch
from app.services.db_service import db_service
from app.models.mongo_models import NoteDoc

@pytest.mark.asyncio
async def test_insert_note():
    note = NoteDoc(title="Test", content="Content", tags=[])
    with patch("app.services.db_service.notes_collection.insert_one", new_callable=AsyncMock) as mock_insert:
        mock_insert.return_value.inserted_id = "abc123"
        note_id = await db_service.insert_note(note)
        assert note_id == "abc123"
