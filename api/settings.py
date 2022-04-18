from pydantic import BaseSettings


class Settings(BaseSettings):
    CLIENT_ID: str
    CLIENT_SECRET: str
    REDIRECT_URI: str = "http://localhost:8000/auth"
    DEFAULT_STREAMER_ID: int = 1968116

    MONGO_URI: str
    MONGO_DB: str

    TEMPLATES_PATH: str

    SOCKET_TOKEN: str
    WEBHOOK_URI: str = "https://discord.com/api/webhooks/963461587191103588/_h6Q21B1Tw6t0GzD_gb0RIVtABhHjGFfC-HeSsNtHGhb6Ln-chRyicFCHkL9E9cOMp4m"

    class Config:
        case_sensitive = True


settings = Settings(_env_file='.env')
