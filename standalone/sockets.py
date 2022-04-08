import asyncio
from datetime import datetime

import socketio

from core.databases.mongo_handler import create_donation, get_streamer
from core.models.donations import Donation

sio = socketio.AsyncClient()


@sio.event
async def connect():
    print('connection established')


@sio.event
async def disconnect():
    print('disconnected from server')


@sio.event
def connect_error(data):
    print("The connection failed!")
    print(data)


@sio.event
def event(data):
    if data['type'] == 'streamlabscharitydonation':
        message = data['message'][0]
        streamer_id = get_streamer({'display_name': message['name']}).user_id
        if streamer_id:
            donation = Donation(donation_id=message['id'], amount=message['amount'], donor=message['from'],
                                message=message['message'])
            create_donation(donation, streamer_id, datetime.fromtimestamp(message['createdAt']))
            print("Donation saved: {}".format(message))
    else:
        print("Not a donation, non pertinent")


async def main():
    await sio.connect('https://sockets.streamlabs.com/?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbiI6IjNGRDY2Qjk3MjI0OERGRDAxM0M4IiwicmVhZF9vbmx5Ijp0cnVlLCJwcmV2ZW50X21hc3RlciI6dHJ1ZSwidHdpdGNoX2lkIjoiOTE1MDcxMDEifQ.75MngQ3iPRpfO6stXpl5iJu4xTP3bkmiVbRIjt1MCOs', transports=['websocket'])
    await sio.wait()


if __name__ == '__main__':
    asyncio.run(main())
