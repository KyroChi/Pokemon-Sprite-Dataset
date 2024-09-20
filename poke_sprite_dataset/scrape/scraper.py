import csv
import os
import re

import requests
from bs4 import BeautifulSoup
from helpers import save_image
from pages import load_homepage, load_pokemon_page
from scrape_poke_api import get_pokemon_from_pokeapi
from tqdm.auto import tqdm
from unwrap_animated_sprites import unwrap_sprite

BASE_URL = "https://bulbapedia.bulbagarden.net"
LANDING = "/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number"


def scrape_bulbapedia(
    config: dict,
    verbose: int = 1,
):
    save_path = config.get("save_path", None)
    if save_path is None:
        raise ValueError("`save_path` must be specified in dataset config.")

    if not os.path.exists(save_path):
        if verbose >= 2:
            print(f"Creating directory: {save_path}")
        os.makedirs(save_path)

    if config.get("full_size", True) and not os.path.exists(
        os.path.join(save_path, "full_size")
    ):
        os.makedirs(os.path.join(save_path, "full_size"))

    if config.get("gen_v_animated_sprites", True) and not os.path.exists(
        os.path.join(save_path, "gen_v_animated_sprites")
    ):
        os.makedirs(os.path.join(save_path, "gen_v_animated_sprites"))

    if config.get("unwrapped_sprites", True) and not os.path.exists(
        os.path.join(save_path, "gen_v_unwrapped_sprites")
    ):
        os.makedirs(os.path.join(save_path, "gen_v_unwrapped_sprites"))

    pokedata = load_homepage(BASE_URL + LANDING)

    if not len(pokedata) == 1025:
        raise Exception(f"Expected 1025 Pokémon, got {len(pokedata)}. Aborting.")

    pokemon_tabular_data = {}

    if config.get("tabular", True):
        for ii in (prog_bar := tqdm(range(len(pokedata)))):
            prog_bar.set_postfix_str(f"Processing Tabular for {pokedata[ii]['name']}")
            pokemon_tabular_data[ii + 1] = get_pokemon_from_pokeapi(ii + 1)

    for ii, pokemon in enumerate((prog_bar := tqdm(pokedata, ncols=100))):
        prog_bar.set_postfix_str(f"Processing {pokemon['name']}")
        page_data = load_pokemon_page(BASE_URL, pokemon)

        if page_data["full_size"] is None:
            continue
        else:
            full_size_filename = os.path.join(
                save_path, "full_size", f"{str(ii + 1).zfill(4)}_{pokemon['name']}.png"
            )
            save_image(page_data["full_size"], full_size_filename)

        gen_v_sprites = page_data["gen_v_animated_sprites"]
        for j, sprite_path in enumerate(gen_v_sprites):
            sprite_filename = sprite_path.split("/")[-1]
            sprite_filename = os.path.join(
                save_path, "gen_v_animated_sprites", f"{sprite_filename}"
            )
            save_image(sprite_path, sprite_filename)
            if config.get("unwrapped_sprites", True):
                unwrap_sprite(
                    sprite_filename, os.path.join(save_path, "gen_v_unwrapped_sprites")
                )

        if config.get("tabular", True):
            pokemon_tabular_data[ii + 1]["shape"] = page_data["shape"]

    if config.get("tabular", True):
        with open(os.path.join(save_path, "poke_tabular.csv"), "w") as f:
            writer = csv.DictWriter(f, fieldnames=list(pokemon_tabular_data[1].keys()))
            writer.writeheader()
            for id in (prog_bar := tqdm(range(1, len(pokemon_tabular_data) + 1))):
                prog_bar.set_postfix_str(
                    f"Writing {pokemon_tabular_data[id]['name']} to CSV"
                )
                writer.writerow(pokemon_tabular_data[id])


if __name__ == "__main__":
    scrape_bulbapedia({"save_path": "/home/kyle/projects/pokemon_data/data"})
