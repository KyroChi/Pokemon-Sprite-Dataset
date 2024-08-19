import requests

# id | name | is_legendary | is_mythical | color | shape | type1 | type2 | egg-group | full_size_images | gen_v_animated_sprites | gen_v_unwrapped_sprites

# Build condition vectors. For each unwrapped sprite and each full size image, we need the following row
# is_legendary | is_mythical | color | shape | type1 | type2 | egg-group

POKEAPI_SPECIES_ENDPOINT = "https://pokeapi.co/api/v2/pokemon-species/"
POKEAPI_TYPE_ENDPOINT = "https://pokeapi.co/api/v2/pokemon/"


def make_request(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(
            f"Failed to get data from {url}, status code: {response.status_code}"
        )


def get_pokemon_from_pokeapi(pokemon_id):
    request_url = f"{POKEAPI_SPECIES_ENDPOINT}{pokemon_id}/"
    species_data = make_request(request_url)

    request_url = f"{POKEAPI_TYPE_ENDPOINT}{pokemon_id}/"
    type_data = make_request(request_url)

    return {
        "id": pokemon_id,
        "name": species_data["name"],
        "is_legendary": species_data["is_legendary"],
        "is_mythical": species_data["is_mythical"],
        "color": species_data["color"]["name"],
        "types": [td["type"]["name"] for td in type_data["types"]],
    }
