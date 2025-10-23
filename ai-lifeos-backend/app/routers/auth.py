from fastapi import APIRouter, HTTPException, status
from app.models.user_model import User
from app.services.auth_service import signup_user, login_user

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup")
async def signup(user: User):
    result = await signup_user(user)
    if "error" in result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"])
    return result

@router.post("/login")
async def login(data: dict):
    email = data.get("email")
    password = data.get("password")
    result = await login_user(email, password)
    if "error" in result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"])
    return result
