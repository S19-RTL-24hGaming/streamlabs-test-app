from typing import List

import requests
from fastapi import HTTPException

from api.settings import settings


def get_token(code: str) -> tuple[str, str]:
    """Makes a request to the streamlabs API to retrieve the users access and refresh tokens

    :param str code: code gotten from the /authorize api call
    :return: tuple with access_token and refresh_token
    """
    body = {
        "grant_type": "authorization_code",
        "client_id": settings.CLIENT_ID,
        "client_secret": settings.CLIENT_SECRET,
        "code": code,
        "redirect_uri": settings.REDIRECT_URI
    }
    r = requests.post("https://streamlabs.com/api/v1.0/token", data=body)
    if r.status_code != 200:
        print(r.request.body)
        raise HTTPException(500, "Something went wrong when requesting your access_token")
    data = r.json()
    return data["access_token"], data["refresh_token"]


def get_user_data(token):
    """Request user data from the streamlabs API

    :param str token: users access_token
    :return: user data in raw json form
    """
    # Why the fuck is this in the query parameters ?
    params = {
        "access_token": token
    }
    r = requests.get("https://streamlabs.com/api/v1.0/user", params=params)
    if r.status_code != 200:
        print(r.status_code, r.text, r.request.body)
        raise HTTPException(500, "Something went wrong when requesting your user data")
    return r.json()


def get_donations(token) -> List:
    """Get all the domations of a particular user from the streamlabs API

    :param str token: users access_token
    :return: json object list containing the donations
    """
    params = {
        "access_token": token
    }
    r = requests.get(f"https://streamlabs.com/api/v1.0/donations", params=params)
    if r.status_code != 200:
        print(r.status_code, r.text, r.request.body)
        raise HTTPException(500, "Something went wrong when requesting your user data")
    return r.json()["data"]


def create_donation(name, message, amount: float, email, token) -> str:
    """Create a donation that is going to be pushed to streamlabs as a real donation. All donations will be
    expressed in EUR for compatibility.

    :param str name: name of the user who donated
    :param str message: message of the user who donated
    :param float amount: amount of money the user donated
    :param str email: email of the user or UID of the donation
    :param str token: access_token of the user
    :return: donation id
    """
    body = {
        "name": name,
        "message": message,
        "identifier": email,
        "amount": amount,
        "currency": "EUR",
        "access_token": token
    }
    r = requests.post("https://streamlabs.com/api/v1.0/donations", data=body)
    if r.status_code != 200:
        print(r.status_code, r.text, r.request.body)
        raise HTTPException(500, "Something went wrong when requesting your user data")
    return r.json()["donation_id"]
