import csv
import os
from dataclasses import asdict, dataclass
from typing import List

from PIL import Image
from torch.utils.data import Dataset
from torchvision.transforms import Resize, ToTensor

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


def parse_sprite(sprite: str) -> tuple[bool, int]:
    chunks = sprite.split("_")
    try:
        pokemon_id = int(chunks[2])
    except Exception as _:
        pokemon_id = int(chunks[2][:-1])

    if len(chunks) == 4:
        is_shiny = True if chunks[3] == "s" else False
    elif len(chunks) == 5:
        is_shiny = True if chunks[4] == "s" else False
    else:
        is_shiny = False
    return is_shiny, pokemon_id


def prepare_png_image(image_path: str) -> Image:
    img = Image.open(image_path).convert("RGBA")
    img = Resize((96, 96))(img)
    return ToTensor()(img)


def list_from_types(types: str) -> List[int]:
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


class GenVUnwrappedSprites(Dataset):
    def __init__(
        self,
        data_dir: str,
        get_shiny: bool = False,
    ):
        self.data_dir = os.path.join(data_dir, "gen_v_unwrapped_sprites")
        self.sprites_list = os.listdir(self.data_dir)
        self.get_shiny = get_shiny

        self.sample_dir = []

        for sprite in self.sprites_list:
            is_shiny, _ = parse_sprite(sprite)

            if not self.get_shiny and is_shiny:
                continue

            for png_file in os.listdir(os.path.join(self.data_dir, sprite)):
                self.sample_dir.append(os.path.join(self.data_dir, sprite, png_file))

    def __getitem__(self, idx):
        return prepare_png_image(self.sample_dir[idx])

    def __len__(self):
        return len(self.sample_dir)


class ConditionalGenVUnwrappedSprites(Dataset):
    def __init__(
        self,
        data_dir: str,
        get_shiny: bool = False,
    ):
        sprites = os.path.join(data_dir, "gen_v_unwrapped_sprites")
        tabular = os.path.join(data_dir, "poke_tabular.csv")
        self.get_shiny = get_shiny

        self.sample_dir = []

        with open(tabular, "r") as f:
            poke_rows = list(csv.DictReader(f))

        for sprite in os.listdir(sprites):
            is_shiny, pokemon_id = parse_sprite(sprite)

            if not self.get_shiny and is_shiny:
                continue

            for png_file in os.listdir(os.path.join(sprites, sprite)):
                self.sample_dir.append(
                    (
                        os.path.join(sprites, sprite, png_file),
                        ConditionalData(
                            name=poke_rows[pokemon_id - 1]["name"],
                            is_legendary=not bool(
                                poke_rows[pokemon_id - 1]["is_legendary"]
                            ),
                            is_mythical=not bool(
                                poke_rows[pokemon_id - 1]["is_mythical"]
                            ),
                            color=color_to_int(poke_rows[pokemon_id - 1]["color"]),
                            shape=poke_rows[pokemon_id - 1]["shape"],
                            types=list_from_types(poke_rows[pokemon_id - 1]["types"]),
                            is_shiny=is_shiny,
                        ),
                    )
                )

    def __getitem__(self, idx):
        sample = self.sample_dir[idx]
        return (prepare_png_image(sample[0]), asdict(sample[1]))

    def __len__(self):
        return len(self.sample_dir)
