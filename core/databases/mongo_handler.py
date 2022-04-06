from fastapi.encoders import jsonable_encoder
from pymongo import MongoClient

from api.settings import settings
from core.models.donations import Donation
from core.models.users import Streamer

client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB]

donations = db['donations']
users = db['users']


def get_donations() -> list[Donation]:
    """Get all donations in the database

    :return: list of donationss
    """
    result = []
    for donation in donations.find({}):
        result.append(Donation(**donation))
    return result


def get_donation(donation_id) -> Donation:
    """Get a donation from the database by using its id

    :param int donation_id: id of the streamlab donation
    :return: donation dict
    """
    if (donation := donations.find_one({'donation_id': donation_id})) is None:
        return None
    return Donation(**donation)


def get_filtered_donations(filters: dict):
    """Get donations in the database by filtering them

    :param filters: dict that contains the mongodb filters
    :return:
    """
    result = []
    for donation in donations.find(filters):
        result.append(donation)
    return result


def create_donation(donation: Donation) -> str:
    """Insert a donation inside of the database

    :param dict donation: donation in the form of a dict
    """
    data = jsonable_encoder(donation)
    _id = donations.insert_one(data).inserted_id
    return _id


def get_users() -> list[Streamer]:
    """Get all users from the Database

    :return: all users in form of dict
    """
    result = []
    for user in users.find({}):
        result.append(Streamer(**user))
    return result


def get_user(user_filter: dict):
    """Get a user by its streamlabs id from the database

    :param dict user_filter: filter for the user
    :return: user data from the database
    """
    if (user := users.find_one(user_filter)) is None:
        return None
    return Streamer(**user)


def get_user_token(username: str) -> str:
    """Get access_token fomr user

    :param str username: name of the user
    :return: access_token
    """
    if (token := users.find_one({'username': username}, {'_id': 0, 'access_token': 1})) is None:
        return ""
    return token


def create_user(user: dict, access_token: str, refresh_token: str, socket_token: str) -> float:
    """Insert a user in the database

    :param dict user: user data
    :param str access_token: user access token
    :param str refresh_token: user refresh token
    :param socket_token: user socket token
    :return: _id of the user document
    """
    data = {"user_id": user['id'], "display_name": user['display_name'], "username": user['username'],
            "access_token": access_token, "refresh_token": refresh_token, "socket_token": socket_token}
    streamer = Streamer(**data)
    data = jsonable_encoder(streamer)
    if users.find_one({'user_id': user['id']}):
        return users.update_one({'user_id': user['id']}, {'$set': data}).upserted_id
    _id = users.insert_one(data).inserted_id
    return _id
