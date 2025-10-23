from passlib.context import CryptContext
from app.models.user_model import User
from app.core.auth_utils import create_access_token
from app.db.database import db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

async def signup_user(user_data: User):
    existing_user = await db["users"].find_one({"email": user_data.email})
    if existing_user:
        return {"error": "User already exists"}

    hashed_pw = hash_password(user_data.password)
    user_dict = user_data.dict()
    user_dict["password"] = hashed_pw
    await db["users"].insert_one(user_dict)
    return {"message": "User created successfully"}

async def login_user(email: str, password: str):
    user = await db["users"].find_one({"email": email})
    if not user:
        return {"error": "User not found"}

    if not verify_password(password, user["password"]):
        return {"error": "Invalid credentials"}

    token = create_access_token({"sub": user["email"]})
    return {"access_token": token, "token_type": "bearer"}
