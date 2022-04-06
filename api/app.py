import requests
from fastapi import FastAPI, Query, Path, Body, HTTPException
from starlette import status

from core.databases.mongo_handler import create_streamer, get_streamer, get_filtered_donations
from api.settings import settings
from core.models.donations import Donation, OutputDonation
from core.models.users import Streamer
from core.streamlabs_handler import get_token, get_user_data, get_socket_token

tags = [
    {
        "name": "Authentication",
        "description": "Operations to authenticate for this API"
    },
    {
        "name": "Streamer",
        "description": "Operations to get streamer data"
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
    create_streamer(user_data['streamlabs'], access_token, refresh_token, socket_token)
    return {"message": "Everything went well, thank you for your help"}


@app.get("/streamer/{username}", tags=["Streamer"], response_model=Streamer)
async def user_data(username: str = Path(..., description="username of the streamer")):
    """Get user data from the database"""
    return get_streamer({'display_name': username})


@app.get("/streamer/{username}/donations", tags=["Streamer"], response_model=list[OutputDonation])
async def user_donations(username: str = Path(..., description="username of the streamer")):
    """Get user donations from the database"""
    user = get_streamer({'display_name': username})
    donations = get_filtered_donations({'streamer_id': user.user_id})
    return donations


@app.post("/streamer/{username}/donations", status_code=status.HTTP_201_CREATED, tags=["Streamer"], response_model=str)
async def create_donation(username: str = Path(..., description="username of the streamer"), donation: Donation = Body(..., description="donation data")):
    """Create a donation for a given user"""
    user_id = get_streamer({'display_name': username}).user_id
    if not user_id:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return create_donation(donation, user_id)


@app.get("/global", tags=["Global"], response_model=dict)
async def global_data():
    """Get global data from the database"""
    return requests.get("https://streamlabscharity.com/api/v1/causes/televie-frs-fnrs").json()
