import sys
sys.dont_write_bytecode = True
import json
from ossapi import Ossapi
api = Ossapi(int(input("Your osu! OAuth API ID: ")), str(input("Your osu! OAuth API Secret: ")))

class Map:
    def __init__(self, id: int):
        self.id = id
        try:
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
        except Exception as e:
            print(f"⚠️  Error fetching map {id}: {e}")
            self.artist = "NOT FOUND"
            self.title = "Map was deleted or unavailable"
            self.mapper = "Unknown"
            self.version = "N/A"
            self.cover = ""
            self.tags = ""
            self.sr = self.od = self.hp = self.bpm = self.drain = 0

def update_maps(data_path: str, skip_existing: bool = True) -> dict:
    with open(data_path) as f:
        data = json.load(f)
    
    existing_ids = set()
    if skip_existing:
        try:
            with open("./data/maps.json", encoding='utf-8') as f:
                existing_ids = {int(id) for id in json.load(f).keys() if id != "0"}
        except FileNotFoundError:
            pass
    
    ids = [id for t in data.values() for p in t['mappools'].values() for id in p.values() if id != 0 and id not in existing_ids]
    maps, missing_ids = {}, []
    
    for id in ids:
        m = Map(id)
        if m.artist == "NOT FOUND":
            missing_ids.append(id)
            print(f"Map {id} not found, replacing with 0")
            # DON'T add the missing ID to maps
        else:
            maps[id] = {k: v for k, v in m.__dict__.items() if k != "id"}
            print(f"Fetched {id}")
    
    # Update pools.json to replace missing IDs with 0
    if missing_ids:
        for p in (pool for t in data.values() for pool in t['mappools'].values()):
            for slot, mid in list(p.items()):
                if mid in missing_ids:
                    p[slot] = 0
        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    
    return maps

maps = update_maps('./data/pools.json')

# Merge with existing maps
try:
    with open("./data/maps.json", encoding='utf-8') as f:
        existing = json.load(f)
        maps.update({k: v for k, v in existing.items() if k not in maps})
except FileNotFoundError:
    pass

# Ensure ID 0 placeholder exists
if "0" not in maps and 0 not in maps:
    maps[0] = {
        "artist": "NOT FOUND",
        "title": "Map was deleted or unavailable",
        "mapper": "Unknown",
        "version": "N/A",
        "cover": "",
        "tags": "",
        "sr": 0,
        "od": 0,
        "hp": 0,
        "bpm": 0,
        "drain": 0
    }

with open("./data/maps.json", 'w', encoding='utf-8') as f:
    json.dump(maps, f, indent=4, ensure_ascii=False)