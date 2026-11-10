from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    GOOGLE_API_KEY: str = ""
    MONGODB_URI: str = "mongodb://localhost:27017"
    MONGODB_DATABASE: str = "support_bot"
    DOCUMENT_ID: str = "apple-support"
    MODEL_NAME: str = "gemini-2.0-flash"
    MAX_INPUT_CHARS: int = 4000

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
