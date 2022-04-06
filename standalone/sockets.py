import asyncio

import socketio

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
    print(data)


async def main():
    await sio.connect('https://sockets.streamlabs.com/?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbiI6IjNGRDY2Qjk3MjI0OERGRDAxM0M4IiwicmVhZF9vbmx5Ijp0cnVlLCJwcmV2ZW50X21hc3RlciI6dHJ1ZSwidHdpdGNoX2lkIjoiOTE1MDcxMDEifQ.75MngQ3iPRpfO6stXpl5iJu4xTP3bkmiVbRIjt1MCOs')
    await sio.wait()


if __name__ == '__main__':
    asyncio.run(main())
