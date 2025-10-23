from pydantic import BaseSettings


class Settings(BaseSettings):
    
    MONGO_URI: str
    REDIS_URL: str

    
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # External API Keys
    ASSEMBLYAI_API_KEY: str
    GEMINI_API_KEY: str
    GOOGLE_CLOUD_PROJECT_ID: str
    GOOGLE_CLOUD_CREDENTIALS_PATH: str

    class Config:
        env_file = ".env"  
        env_file_encoding = "utf-8"


# Create a config instance
config = Settings()
