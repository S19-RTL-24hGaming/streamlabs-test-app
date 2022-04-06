from pymongo import MongoClient

from api.settings import settings

client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB]

donations = db['donations']
users = db['users']


def get_donations():
    """Get all donations in the database

    :return: list of donationss
    """
    result = []
    for donation in donations.find({}):
        result.append(donation)
    return result


def get_donation(donation_id) -> dict:
    """Get a donation from the database by using its id

    :param int donation_id: id of the streamlab donation
    :return: donation dict
    """
    if (donation := donations.find_one({'donation_id': donation_id}, {'_id': 0})) is None:
        return {}
    return donation


def get_filtered_donations(filters: dict):
    """Get donations in the database by filtering them

    :param filters: dict that contains the mongodb filters
    :return:
    """
    result = []
    for donation in donations.find(filters, {'_id': 0}):
        result.append(donation)
    return result


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
    result = []
    for user in users.find({}):
        result.append(user)
    return result


def get_user(user_filter: dict):
    """Get a user by its streamlabs id from the database

    :param dict user_filter: filter for the user
    :return: user data from the database
    """
    if (user := users.find_one(user_filter, {'_id': 0})) is None:
        return {}
    return user


def get_user_token(username: str) -> str:
    """Get access_token fomr user

    :param str username: name of the user
    :return: access_token
    """
    if (token := users.find_one({'username': username}, {'_id': 0, 'access_token': 1})) is None:
        return ""
    return token


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
