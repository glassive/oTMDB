## osu!taiko Mappool Database

How to use [update.py](/tools/update.py):
```shell
cd tools
py -m venv .venv; .venv\scripts\activate; pip install -r .\requirements.txt
```

Run the script. This will fetch all map data corresponding to the mappools in [pools.json](/data/pools.json).

[ossapi docs](https://tybug.dev/ossapi/index.html)

todo: refer to [ikin's repo](https://github.com/ikin5050/osuPoolCheck) for tournament data

consider db exporting later on for convenience (mysql or sqlite)

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
