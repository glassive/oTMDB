import sys
sys.dont_write_bytecode = True
import json
from ossapi import Ossapi

API_ID = int(input("Your osu! OAuth API ID: "))
API_SECRET = str(input("Your osu! OAuth API Secret: "))

api = Ossapi(API_ID, API_SECRET)

class Map:
    """Fetches the beatmap API endpoint with a given ID when instantiated and stores relevant data."""
    def __init__(self, id: int):
        self.id = id
        data = api.beatmap(id)
        mapset = data._beatmapset

        self.artist = mapset.artist
        self.title = mapset.title
        self.mapper = mapset.creator
        self.version = data.version
        self.cover = mapset.covers.card_2x
        self.tags = mapset.tags
        self.sr = data.difficulty_rating
        self.od = data.accuracy
        self.hp = data.drain
        self.bpm = data.bpm
        self.drain = data.hit_length

FILENAME = "./data/maps.json"

def update_maps(data_path: str) -> dict:
    # load tourneys json
    with open(data_path, 'r') as f:
        data = json.load(f)

    # grab all map ids and re-fetch data (with the API call in the Map class)
    ids = [id for tournament in data.values() for pool in tournament['mappools'].values() for id in pool.values()]
    maps = {}
    for id in ids:
        maps[id] = {k: v for k, v in Map(id).__dict__.items() if k != "id"}
        print(f"Fetched {id}")
    return maps


maps = update_maps('./data/pools.json')

# write to output file
with open(FILENAME, 'w', encoding='utf-8') as f:
    json.dump(maps, f, indent=4, ensure_ascii=False)