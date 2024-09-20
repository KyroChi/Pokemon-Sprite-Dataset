import csv
import os

from datasets import Dataset as HFDataset
from datasets import Image

from .helpers import embed_poke_row

def _get_full_art_dataset(
    path: str,    
):
    img_paths = []
    conditions = []

    full_size_path = os.path.join(path, "full_size")
    tabular = os.path.join(path, "poke_tabular.csv")

    with open(tabular, "r") as f:
        poke_rows = list(csv.DictReader(f))

    for pokemon in os.listdir(full_size_path):
        poke_id = int(pokemon.split("_")[0])
        img_paths.append(os.path.join(full_size_path, pokemon))
        conditions.append(embed_poke_row(poke_rows[poke_id - 1]))

    return img_paths, conditions

def full_art_dataset(
        path: str=None,
        conditional: bool=False,
        *args, **kwargs
):
    img_paths, conditions = _get_full_art_dataset(path)

    if conditional:
        return HFDataset.from_dict({
            "image": img_paths,
            "condition": conditions
        }, *args, **kwargs).cast_column("image", Image())
    else:
        return HFDataset.from_dict({
            "image": img_paths
        }, *args, **kwargs).cast_column("image", Image())