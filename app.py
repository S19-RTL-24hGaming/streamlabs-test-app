import json
import os.path

from fastapi import FastAPI, Query
from starlette import status

from settings import settings
from streamlabs_handler import get_token, get_user_data

tags = [
    {
        "name": "Authentication",
        "description": "Operations to authenticate for this API"
    },
]

app = FastAPI(
    title="TelevieAPI",
    description="API for the 24H stream marathon of the Televie. This page is strictly confidential.",
    version="1.0.0",
    openapi_tags=tags
)


def save_token(username, token):
    if os.path.exists('data.json') and os.path.getsize('data.json'):
        with open('data.json', 'r+') as f:
            data = json.load(f)
            data[username] = token
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
    else:
        with open('data.json', 'w+') as f:
            data = {username: token}
            f.seek(0)
            json.dump(data, f, indent=4)


@app.get("/link", status_code=status.HTTP_200_OK, tags=["Authentication"])
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
    username = user_data["streamlabs"]["username"]
    save_token(username, access_token)
    return {"message": "Everything went well, thank you for your help"}

