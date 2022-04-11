from datetime import datetime

import requests
from fastapi.encoders import jsonable_encoder
# from motor.motor_asyncio import AsyncIOMotorClient

from api.settings import settings
from core.databases.mongo_handler import db
from core.models.donations import Donation, OutputDonation


# client = AsyncIOMotorClient(settings.MONGO_URI)
# as_db = client[settings.MONGO_DB]
# async_donations = as_db.test_donations

donations = db['test_donations']


# async def create_donation_async(donation: Donation, streamer_id: int, created_at: datetime = None) -> str:
#     """Insert a donation inside of the database
#
#     :param donation: donation in the form of a Donation object
#     :param streamer_id: id of the streamer
#     :param created_at: datetime of the donation
#     """
#     if created_at:
#         don = OutputDonation(**donation.dict(), streamer_id=streamer_id, created_at=created_at)
#     else:
#         don = OutputDonation(**donation.dict(), streamer_id=streamer_id, created_at=datetime.now())
#     data = jsonable_encoder(don)
#     _id = async_donations.insert_one(data).inserted_id
#     return _id


# async def process_donation_async(result: dict):
#     """Process a donation
#
#     :param dict result: donation dat fron the API
#     """
#     donation_data = result["donation"]
#     streamer_id = int(result["member"]["user"]['id'])
#     message = donation_data["comment"]["text"] if donation_data["comment"] else ""
#     donation = Donation(donation_id=donation_data['id'], amount=float(donation_data['converted_amount']) / 100,
#                         donor=donation_data['display_name'], message=message)
#     await create_donation_async(donation, streamer_id,
#                                 datetime.strptime(donation_data['created_at'][:-6], "%Y-%m-%dT%H:%M:%S"))


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


def process_donation(result: dict):
    """Process a donation

    :param dict result: donation dat fron the API
    """
    donation_data = result["donation"]
    streamer_id = int(result["member"]["user"]['id']) if result["member"] else settings.DEFAULT_STREAMER_ID
    message = donation_data["comment"]["text"] if donation_data["comment"] else ""
    donation = Donation(donation_id=donation_data['id'], amount=float(donation_data['converted_amount']) / 100,
                        donor=donation_data['display_name'], message=message)
    create_donation(donation, streamer_id, datetime.strptime(donation_data['created_at'][:-6], "%Y-%m-%dT%H:%M:%S"))


def get_team_donations(team_id: str, donation_id: str = None):
    """Get all donations from a charity team

    :param str team_id: ID of the team
    :param str donation_id: ID of the donation to start from
    """
    if donation_id:
        url = f"https://streamlabscharity.com/api/v1/teams/{team_id}/donations?id={donation_id}"
    else:
        url = f"https://streamlabscharity.com/api/v1/teams/{team_id}/donations"
    response = requests.get(url)
    if response.status_code != 200:
        print(response.status_code, response.text, response.headers)
        return
    data = response.json()
    for result in data:
        try:
            process_donation(result)
            # process_donation_async(result)
        except Exception as e:
            print(e)
            print(result)


if __name__ == '__main__':
    get_team_donations("337671010314752000")
