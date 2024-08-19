import os

from apnggif import apnggif
from PIL import Image


def unwrap_sprite(source_file, destination_folder):
    """
    Unwrap the animated sprites into individual frames.

    Args:
        source_file (str): The path to the animated sprite.
        destination_folder (str): The folder to save the individual frames.
    """
    base_name = source_file.split(".")[0]
    base_name = ".".join([base_name, "gif"])
    if not os.path.exists(base_name):
        apnggif(source_file, base_name)

    gif = Image.open(base_name)

    file_name = source_file.split("/")[-1].split(".")[0]
    dir_name = os.path.join(destination_folder, f"{file_name}")
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    if hasattr(gif, "n_frames"):
        for i in range(gif.n_frames):
            gif.seek(i)
            gif.save(os.path.join(destination_folder, dir_name, f"{i}.png"))
