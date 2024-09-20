# Pokémon Sprite and Image Dataset for Conditional Generation

This dataset contains sprites, animated sprites, Bulbapedia artworks, and tabular data for all of the Pokémon listed on Bulbapdia.

This dataset is built on the back of the [Bulbapeida](https://bulbapedia.bulbagarden.net/wiki/Main_Page) and the [PokéAPI](https://pokeapi.co/). It aggregates the resources that I required for building a generative diffusion model for Pokémon sprite animations.

Note that all of the sprites are owned by Nintendo... so use at your own risk!

## Getting Started
Clone the repo and then run
```
conda env create -f environment.yml 
conda activate poke_sprite_dataset
```
to set up the conda environment, and run 
```
python setup.py install
```
to install as a module.

Next run
```
python build_dataset.py
```
to download the data and create a data directory.

From here you should be able to look at `example/` for some demo notebooks and then load the data in your own progrmas.

Enjoy!

<!-- ## Contributer Setup
```
pip install pre-commit
pre-commit install
```
Then before a push you can run
```
pre-commit run --all-files
``` -->
