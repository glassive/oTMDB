import json
import requests
import argparse
from bs4 import BeautifulSoup

MOD_PREFIX = {
    "NoMod": "NM",
    "Hidden": "HD",
    "HardRock": "HR",
    "DoubleTime": "DT",
    "FreeMod": "FM",
    "Tiebreaker": "TB",
    "HalfTime": "HT",
    "EX": "EX"
}

HEADERS = {"User-Agent": "osu-wiki-mappool-parser/1.0"}


def get_soup(url: str) -> BeautifulSoup:
    r = requests.get(url, headers=HEADERS, timeout=15)
    r.raise_for_status()
    try:
        return BeautifulSoup(r.text, "lxml")
    except Exception:
        return BeautifulSoup(r.text, "html.parser")

def extract_beatmap_id(href: str) -> int:
    # href always ends with .../<beatmap_id>
    return int(href.rstrip("/").split("/")[-1])

def parse_mappools(wiki_url: str, tournament_name: str) -> dict:
    soup = get_soup(wiki_url)

    result = {tournament_name: {"forum": wiki_url, "mappools": {}}}

    mappools_h2 = soup.find("h2", id="mappools")
    if not mappools_h2:
        raise RuntimeError("Mappools section not found")
    node = mappools_h2.find_next_sibling()

    # Iterate until the next <h2>
    while node and node.name != "h2":
        if node.name == "h3":
            stage_name = node.get_text(strip=True)
            result[tournament_name]["mappools"][stage_name] = {}

            ul = node.find_next_sibling("ul")
            if not ul:
                node = node.find_next_sibling()
                continue

            for mod_li in ul.find_all("li", recursive=False):
                mod_div = mod_li.find("div", recursive=False)
                if not mod_div:
                    continue

                # First text node = mod name
                mod_name = mod_div.find(text=True, recursive=False)
                if not mod_name:
                    continue

                mod_name = mod_name.strip()
                prefix = MOD_PREFIX.get(mod_name)
                if not prefix:
                    continue

                ol = mod_div.find("ol")
                if not ol:
                    continue

                maps = ol.find_all("li", recursive=False)

                for i, map_li in enumerate(maps, start=1):
                    a = map_li.find("a", href=True)
                    if not a:
                        continue

                    beatmap_id = extract_beatmap_id(a["href"])

                    if prefix == "TB":
                        slot = "TB"
                    else:
                        slot = f"{prefix}{i}"

                    result[tournament_name]["mappools"][stage_name][slot] = beatmap_id

        node = node.find_next_sibling()

    mappools = result[tournament_name]["mappools"]

    result[tournament_name]["mappools"] = dict(
        reversed(mappools.items())
    )
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract osu! tournament mappools from wiki pages")
    parser.add_argument("url", help="osu! wiki tournament URL")
    parser.add_argument("tournament_name", help="Tournament name used as JSON root key")
    parser.add_argument("-o", "--output", help="Write output JSON to file instead of stdout")
    args = parser.parse_args()
    data = parse_mappools(args.url, args.tournament_name)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    else:
        print(json.dumps(data, indent=4))
