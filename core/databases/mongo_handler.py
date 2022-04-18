from datetime import datetime
from typing import Union

from fastapi.encoders import jsonable_encoder
from pymongo import MongoClient

from api.settings import settings
from core.models.donations import Donation, OutputDonation
from core.models.streamers import Streamer, DatabaseStreamer

client = MongoClient(settings.MONGO_URI, connectTimeoutMS=5000)
db = client[settings.MONGO_DB]

donations = db['donations']
users = db['streamers']


def get_donations() -> list[OutputDonation]:
    """Get all donations in the database

    :return: list of donationss
    """
    result = []
    for donation in donations.find({}):
        result.append(OutputDonation(**donation))
    return result


def get_donation(donation_id) -> Union[OutputDonation, None]:
    """Get a donation from the database by using its id

    :param int donation_id: id of the streamlab donation
    :return: donation dict
    """
    if (donation := donations.find_one({'donation_id': donation_id})) is None:
        return None
    return OutputDonation(**donation)


def get_filtered_donations(filters: dict) -> list[OutputDonation]:
    """Get donations in the database by filtering them

    :param filters: dict that contains the mongodb filters
    :return:
    """
    result = []
    for donation in donations.find(filters):
        result.append(OutputDonation(**donation))
    return result


def get_donations_scoreboard() -> list[Donation]:
    """Get the top donations in form of a scoreboard"""
    result = []
    for donation in donations.find({}).sort('amount', -1).limit(10):
        result.append(Donation(**donation))
    return result


def create_donation(donation: Donation, streamer_id: int, created_at: datetime = None) -> str:
    """Insert a donation inside of the database

    :param donation: donation in the form of a Donation object
    :param streamer_id: id of the streamer
    :param created_at: datetime of the donation
    """
    if created_at:
        don = OutputDonation(**donation.dict(), streamer_id=streamer_id, created_at=created_at)
    else:
        don = OutputDonation(**donation.dict(), streamer_id=streamer_id, created_at=datetime.now())
    data = jsonable_encoder(don)
    _id = donations.insert_one(data).inserted_id
    return _id


def get_streamers() -> list[Streamer]:
    """Get all streamers from the Database

    :return: all streamers in form of dict
    """
    result = []
    for user in users.find({}):
        result.append(Streamer(**user))
    return result


def get_streamer(user_filter: dict) -> Union[Streamer, None]:
    """Get a streamer by its streamlabs id from the database

    :param dict user_filter: filter for the streamer
    :return: streamer data from the database
    """
    if (user := users.find_one(user_filter)) is None:
        return None
    return Streamer(**user)


def get_streamer_token(username: str) -> str:
    """Get access_token for streamer

    :param str username: name of the streamer
    :return: access_token
    """
    if (token := users.find_one({'username': username}, {'_id': 0, 'access_token': 1})) is None:
        return ""
    return token


def create_streamer(user: dict) -> str:
    """Insert a streamer in the database

    :param dict user: user data
    :return: _id of the streamer document
    """
    goal = user["goal"]["amount"] if user["goal"] else 0
    data = {"team_member_id": user['id'], "user_id": user["user"]["id"], "goal": goal,
            "display_name": user["user"]['display_name'], "username": user["user"]['slug']}
    streamer = DatabaseStreamer(**data, created_at=datetime.now(), updated_at=datetime.now())
    encoded = jsonable_encoder(streamer)
    if (existing_user := users.find_one({'user_id': streamer.user_id})) is not None:
        existing_user = DatabaseStreamer(**existing_user)
        update_model = existing_user.copy(update=data)
        update_model.updated_at = datetime.now()
        update_encode = jsonable_encoder(update_model)
        return users.update_one({'user_id': existing_user.user_id}, {'$set': update_encode}).upserted_id
    _id = users.insert_one(encoded).inserted_id
    return _id
