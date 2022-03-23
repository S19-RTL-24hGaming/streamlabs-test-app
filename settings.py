from pydantic import BaseSettings


class Settings(BaseSettings):
    CLIENT_ID: str
    CLIENT_SECRET: str
    REDIRECT_URI: str = "http://localhost:8000/auth"

    class Config:
        case_sensitive = True


settings = Settings(_env_file='.env')
