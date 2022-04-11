from pydantic import BaseSettings


class Settings(BaseSettings):
    CLIENT_ID: str
    CLIENT_SECRET: str
    REDIRECT_URI: str = "http://localhost:8000/auth"
    DEFAULT_STREAMER_ID: int = 1968116

    MONGO_URI: str
    MONGO_DB: str

    BASE_PATH: str

    class Config:
        case_sensitive = True


settings = Settings(_env_file='.env')
