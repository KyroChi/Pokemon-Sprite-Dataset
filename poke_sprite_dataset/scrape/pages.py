import re

import requests
from bs4 import BeautifulSoup
from poke_sprite_dataset.scrape.helpers import get_generation

POKETYPES = [
    "Normal",
    "Fire",
    "Water",
    "Electric",
    "Grass",
    "Ice",
    "Fighting",
    "Poison",
    "Ground",
    "Flying",
    "Psychic",
    "Bug",
    "Rock",
    "Ghost",
    "Dragon",
    "Dark",
    "Steel",
    "Fairy",
]


def load_homepage(url):
    response = requests.get(url)

    pokemon_data = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        rows = soup.find_all("tr", style="background:#FFF")

        for row in rows:
            # Currently this cannot handle pokemon with multiple forms
            try:
                cells = row.find_all("td")
                if cells[0].get("rowspan"):
                    id_num = int(
                        cells[0].get_text(strip=True)[1:]
                    )  # Remove the '#' and convert to int
                    name = cells[2].find("a").get_text(strip=True)
                    link = cells[2].find("a")["href"]
                    type_cells = []
                    for a in cells[3:]:
                        type_cells += a.find_all("a")
                    types = [a.get_text(strip=True) for a in type_cells]
                    pokemon_data.append(
                        {
                            "id": id_num,
                            "name": name,
                            "link": link,
                            "type": types,
                            "generation": get_generation(id_num),
                        }
                    )
            except Exception as e:
                print(row)
                print(e)
                print(f"Failed to parse row: {row}")
        return pokemon_data
    else:
        raise Exception(
            f"Failed to get data from {url}, status code: {response.status_code}"
        )


def load_pokemon_page(base_url, pokemon):
    wiki_url = base_url + pokemon["link"]
    response = requests.get(wiki_url)

    return_data = {
        "full_size": None,
        "gen_v_animated_sprites": None,
        "gen_vi_sprites": None,
        "gen_vii_sprites": None,
        "gen_viii_sprites": None,
        "pokedex_entries": [],
        "stage": None,
    }

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        if pokemon["name"] == "Wormadam":
            td = soup.find("a", {"class": "image", "title": "Plant Cloak"})
        else:
            td = soup.find("a", {"class": "image", "title": pokemon["name"].title()})
        if not td:
            print(f"Failed to find image for {pokemon['name']} at {wiki_url}")
            # print(soup.find_all('a', {'class': 'image'}))
            # raise Exception(f"Failed to find image for {pokemon['name']} at {wiki_url}")

        # TODO: Also grab the mega versions of the pokemon
        try:
            return_data["full_size"] = td.find("img")["src"]
        except:
            print(f"Failed to find full size image for {pokemon['name']} at {wiki_url}")
            return_data["full_size"] = None
 
        pattern = re.compile(r"/wiki/File:Spr_5b_.*")
        matches = soup.find_all("a", href=pattern)

        files = []
        for match in matches:
            try:
                files.append(match.find("img")["src"])
            except:
                print(f'Failed to find gen_v sprite for {pokemon["name"]}')
        return_data["gen_v_animated_sprites"] = files

        pattern = re.compile(r"File:Body\d{2}.png")
        matches = soup.find_all("a", href=pattern)

        # BS can sometimes grad more than one match... I am hoping that the first is
        # always the correct one
        body_type = matches[0]["href"].split(".")[-2][-2:]

        return_data["shape"] = int(body_type)

        return return_data
    else:
        raise Exception(
            f"Failed to get data from {wiki_url}, status code: {response.status_code}"
        )
