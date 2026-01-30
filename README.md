## osu!taiko Mappool Database

How to use the scripts in [/tools](/tools/):
```shell
cd tools
py -m venv .venv; .venv\scripts\activate; pip install -r .\requirements.txt

# extract a tournament from a wiki page (only works with tournaments referenced in the wiki)
python .\tools\extract_pools.py "https://osu.ppy.sh/wiki/en/Tournaments/GTS/IGTS_2022" "IGTS 2022" -o igts2022.json
# then, append the output to pools.json

# fetch all maps from the new pools.json
python .\tools\update.py <id> <secret>
```

[ossapi docs](https://tybug.dev/ossapi/index.html)

refer to [ikin's repo](https://github.com/ikin5050/osuPoolCheck) for tournament data



Tournament JSON template:
```json
{
    "Tournament Name": {
        "forum": "https://link-to-forum.post",
        "mappools": {
            "Stage Name": {
                "NM1": 4092828,
                "NM2": 4092828,
                "NM3": 4092828,
                "NM4": 4092828,
                "NM5": 4092828,
                "NM6": 4092828,
                "HD1": 4092828,
                "HD2": 4092828,
                "HR1": 4092828,
                "HR2": 4092828,
                "DT1": 4092828,
                "DT2": 4092828,
                "FM1": 4092828,
                "FM2": 4092828,
                "FM3": 4092828,
                "TB": 4092828
            }
        }
    }
}
```
(Slot name: Map ID)

## Missing Maps

Many older tournaments will have a handful of missing maps. I try to manually check most of them, but if you happen to find a map that was marked as missing, please let me know.

##To-do

- Search feature (by artist, title, mapper, version, tags)
- consider db exporting later on (mysql or sqlite)
- consistent scrollbar across browsers?
- get a better exhaustive tournament list