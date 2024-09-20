import torch

from dataclasses import dataclass
from typing import List

def white_background(image):
    """
        image is expected to be a PIL Image object
    """
    data = image.getdata()
    new_data = []
    for item in data:
        if item[3] == 0:
            new_data.append((255, 255, 255, 255))
        else:
            new_data.append(item)
    image.putdata(new_data)
    return image.convert("RGB")

TYPE_TO_INT_MAP = {
    "normal": 0,
    "fighting": 1,
    "flying": 2,
    "poison": 3,
    "ground": 4,
    "rock": 5,
    "bug": 6,
    "ghost": 7,
    "steel": 8,
    "fire": 9,
    "water": 10,
    "grass": 11,
    "electric": 12,
    "psychic": 13,
    "ice": 14,
    "dragon": 15,
    "dark": 16,
    "fairy": 17,
}

INT_TO_TYPE_MAP = {
    0: "normal",
    1: "fighting",
    2: "flying",
    3: "poison",
    4: "ground",
    5: "rock",
    6: "bug",
    7: "ghost",
    8: "steel",
    9: "fire",
    10: "water",
    11: "grass",
    12: "electric",
    13: "psychic",
    14: "ice",
    15: "dragon",
    16: "dark",
    17: "fairy",
}

COLOR_TO_INT_MAP = {
    "black": 0,
    "blue": 1,
    "brown": 2,
    "gray": 3,
    "green": 4,
    "pink": 5,
    "purple": 6,
    "red": 7,
    "white": 8,
    "yellow": 9,
}

INT_TO_COLOR_MAP = {
    0: "black",
    1: "blue",
    2: "brown",
    3: "gray",
    4: "green",
    5: "pink",
    6: "purple",
    7: "red",
    8: "white",
    9: "yellow",
}


def type_to_int(type: str) -> int:
    return TYPE_TO_INT_MAP[type]


def int_to_type(int_type: int) -> str:
    return INT_TO_TYPE_MAP[int_type]


def color_to_int(color):
    return COLOR_TO_INT_MAP[color]


def int_to_color(color):
    return INT_TO_COLOR_MAP[color]

def list_from_types(types: str):
    # Input will be a string like "['normal', ' fire']". We have to
    # strip the brackets, split by comma, strip the quotes and
    # whitespace, and map to integers.
    return [type_to_int(t.strip()[1:-1]) for t in types[1:-1].split(",")]

@dataclass
class ConditionalData:
    name: str
    is_legendary: bool
    is_mythical: bool
    color: int
    shape: int
    types: List[int]
    is_shiny: bool

def embed(cond):
    vec = torch.zeros(7)

    vec[0] = 1. if cond['is_legendary'] else 0.5
    vec[1] = 1. if cond['is_mythical'] else 0.5
    vec[2] = (float(cond['color']) + 1.) / 10.
    vec[3] = float(cond['shape']) / 14.
    vec[4] = (float(cond['types'][0]) + 1.) / 18.
    vec[5] = (float(cond['types'][0]) + 1.) / 18. if len(cond['types']) == 1 else (float(cond['types'][1]) + 1.) / 18.
    vec[6] = 1. if cond['is_shiny'] else 0.5

    return vec

def unwrap_embedding(embedding):
    return ConditionalData(
        name="",
        is_legendary=embedding[0] > 0.75,
        is_mythical=embedding[1] > 0.75,
        color=int_to_color(int(embedding[2] * 10 - 1)),
        shape=int(embedding[3] * 14),
        types=[int_to_type(int(embedding[4] * 18 - 1 + 0.5)), 
               int_to_type(int(embedding[5] * 18 - 1 + 0.5))],
        is_shiny=embedding[6] > 0.75,
    )

def embed_poke_row(poke_data):
    return embed(dict(
        name=poke_data["name"],
        is_legendary=not bool(poke_data["is_legendary"]),
        is_mythical=not bool(poke_data["is_mythical"]),
        color=color_to_int(poke_data["color"]),
        shape=poke_data["shape"],
        types=list_from_types(poke_data["types"]),
        is_shiny=False,
    ))