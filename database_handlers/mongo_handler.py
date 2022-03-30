from typing import Optional

from pymongo import MongoClient

from settings import settings

client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB]

donations = db['donations']
users = db['users']


def get_donations():
    """Get all donations in the database

    :return: list of donationss
    """
    return donations.find({})


def get_donation(donation_id) -> dict:
    """Get a donation from the database by using its id

    :param int donation_id: id of the streamlab donation
    :return: donation dict
    """
    return donations.find_one({'donation_id': donation_id})


def get_filtered_donations(filters: dict):
    """Get donations in the database by filtering them

    :param filters: dict that contains the mongodb filters
    :return:
    """
    return donations.find(filters)


def create_donation(donation: dict):
    """Insert a donation inside of the database

    :param dict donation: donation in the form of a dict
    """
    _id = donations.insert_one(donation).inserted_id
    return _id


def get_users():
    """Get all users from the Database

    :return: all users in form of dict
    """
    return users.find({})


def get_user(user_filter: dict):
    """Get a user by its streamlabs id from the database

    :param dict user_filter: filter for the user
    :return: user data from the database
    """
    return users.find_one(user_filter)


def get_user_token(username: str) -> str:
    """Get access_token fomr user

    :param str username: name of the user
    :return: access_token
    """
    return users.find({'display_name': username}, {'access_token': 1})


def create_user(user: dict, access_token: str, refresh_token: str) -> float:
    """Insert a user in the database

    :param str refresh_token: user refresh token
    :param str access_token: user access token
    :param dict user: user data
    :return: _id of the user document
    """
    data = {"user_id": user['id'], "display_name": user['display_name'], "username": user['username'],
            "access_token": access_token, "refresh_token": refresh_token}
    if users.find_one({'user_id': user['id']}):
        return users.update_one({'user_id': user['id']}, {'$set': data}).upserted_id
    _id = users.insert_one(data).inserted_id
    return _id
