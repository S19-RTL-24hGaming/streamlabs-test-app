import requests
from fastapi import FastAPI, Query
from starlette import status

from core.databases.mongo_handler import create_user, get_user
from api.settings import settings
from core.models.users import Streamer
from core.streamlabs_handler import get_token, get_user_data, get_socket_token

tags = [
    {
        "name": "Authentication",
        "description": "Operations to authenticate for this API"
    },
    {
        "name": "User",
        "description": "Operations to get user data"
    }
]

app = FastAPI(
    title="TelevieAPI",
    description="API for the 24H stream marathon of the Televie. This page is strictly confidential.",
    version="1.0.0",
    openapi_tags=tags
)


@app.get("/link", tags=["Authentication"])
async def authorize_link():
    """Get the authorization link that streamers need to click to connect to our application"""
    link = "https://www.streamlabs.com/api/v1.0/authorize?client_id=" + settings.CLIENT_ID
    link += "&redirect_uri=" + settings.REDIRECT_URI
    link += "&response_type=code"
    link += "&scope=donations.read+donations.create+alerts.create+socket.token+alerts.write+profiles.write+jar.write" \
            "+wheel.write+mediashare.control+credits.write"
    return link


@app.get("/auth", status_code=status.HTTP_201_CREATED, tags=["Authentication"])
async def authorize(code: str = Query(..., description="code given from the authorization of the user")):
    """Callback url for our application to get user token when authorizing connection to our app"""
    access_token, refresh_token = get_token(code)
    user_data = get_user_data(access_token)
    socket_token = get_socket_token(access_token)
    create_user(user_data['streamlabs'], access_token, refresh_token, socket_token)
    return {"message": "Everything went well, thank you for your help"}


@app.get("/user", tags=["User"], response_model=Streamer)
async def user_data(username: str = Query(..., description="username of the user")):
    """Get user data from the database"""
    user = get_user({'display_name': username})
    if not user:
        return {}
    return user


@app.get("/global", tags=["Global"], response_model=dict)
async def global_data():
    """Get global data from the database"""
    return requests.get("https://streamlabscharity.com/api/v1/causes/televie-frs-fnrs").json()
