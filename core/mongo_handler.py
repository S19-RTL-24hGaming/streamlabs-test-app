from datetime import datetime
from typing import Union

from fastapi.encoders import jsonable_encoder
# from pymongo import MongoClient



# from motor_asyncio import AsyncIOMotorClient
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient 



from api.settings import settings
from core.models.donations import Donation, OutputDonation
from core.models.streamers import Streamer, DatabaseStreamer

client = AsyncIOMotorClient(settings.MONGO_URI)
db = client[settings.MONGO_DB]

donations = db['donations']
users = db['streamers']

async def get_donations() -> list[OutputDonation]:
	"""Get all donations in the database

	:return: list of donationss
	"""
	result = []
	for donation in await donations.find({}):
		result.append(OutputDonation(**donation))
	return result


async def get_donation(donation_id) -> Union[OutputDonation, None]:
	"""Get a donation from the database by using its id

	:param int donation_id: id of the streamlab donation
	:return: donation dict
	"""
	donation = await donations.find_one({'donation_id': donation_id})
	if (donation is None):
		return None
	return OutputDonation(**donation)


async def get_filtered_donations(filters: dict) -> list[OutputDonation]:
	"""Get donations in the database by filtering them

	:param filters: dict that contains the mongodb filters
	:return:
	"""
	result = []
	for donation in await donations.find(filters):
		result.append(OutputDonation(**donation))
	return result


async def get_donations_scoreboard() -> list[Donation]:
	"""Get the top donations in form of a scoreboard"""
	result = []
	for donation in await donations.find({}).sort('amount', -1).limit(10):
		result.append(Donation(**donation))
	return result


async def create_donation(donation: Donation, streamer_id: int, created_at: datetime = None) -> str:
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
	test_donation = await get_donation(data['donation_id'])
	if test_donation == None:
		test = await donations.insert_one(data)
		return test.inserted_id
	return test_donation.id


async def get_streamers() -> list[Streamer]:
	"""Get all streamers from the Database

	:return: all streamers in form of dict
	"""
	result = []
	for user in await users.find({}):
		result.append(Streamer(**user))
	return result


async def get_streamer(user_filter: dict) -> Union[Streamer, None]:
	"""Get a streamer by its streamlabs id from the database

	:param dict user_filter: filter for the streamer
	:return: streamer data from the database
	"""
	user = await users.find_one(user_filter)
	if (user is None):
		return None
	return Streamer(**user)


async def get_streamer_token(username: str) -> str:
	"""Get access_token for streamer

	:param str username: name of the streamer
	:return: access_token
	"""
	token = await users.find_one({'username': username}, {'_id': 0, 'access_token': 1})
	if (token is None):
		return ""
	return token


async def create_streamer(user: dict, access_token: str, refresh_token: str, socket_token: str) -> str:
	"""Insert a streamer in the database

	:param dict user: user data
	:param str access_token: streamer access token
	:param str refresh_token: streamer refresh token
	:param socket_token: streamer socket token
	:return: _id of the streamer document
	"""
	data = {"user_id": user['id'], "display_name": user['display_name'], "username": user['username'],
			"access_token": access_token, "refresh_token": refresh_token, "socket_token": socket_token}
	streamer = DatabaseStreamer(**data, created_at=datetime.now(), updated_at=datetime.now())
	data = jsonable_encoder(streamer)
	if await users.find_one({'user_id': user['id']}):
		return await users.update_one({'user_id': user['id']}, {'$set': data}).upserted_id
	_id = await users.insert_one(data).inserted_id
	return _id
