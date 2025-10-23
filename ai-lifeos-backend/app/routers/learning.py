from fastapi import APIRouter
from app.services.gemini_service import gemini_service
from app.models.schemas import LearningSuggestionRequest, LearningSuggestionResponse

router = APIRouter(prefix="/api/learning", tags=["learning"])

@router.post("/suggest", response_model=LearningSuggestionResponse)
async def get_suggestion(request: LearningSuggestionRequest):
    """Get personalized learning suggestion via Gemini."""
    data = await gemini_service.generate_learning_suggestion(request.user_input)
    return LearningSuggestionResponse(**data)