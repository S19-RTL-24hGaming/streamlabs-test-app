import requests

from core.databases.mongo_handler import create_streamer


def process_streamers(streamers: list):
    for streamer in streamers:
        try:
            create_streamer(streamer)
        except Exception as e:
            print(e, streamer)


def get_streamers(team_id: str):
    response = requests.get(f"https://streamlabscharity.com/api/v1/teams/{team_id}/members")
    data = response.json()
    next_url = data["next_page_url"]
    process_streamers(data["data"])
    while next_url:
        r = requests.get(next_url)
        json = r.json()
        next_url = json["next_page_url"]
        process_streamers(json["data"])


if __name__ == '__main__':
    get_streamers("337671010314752000")
