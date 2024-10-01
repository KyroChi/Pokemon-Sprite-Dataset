# Pokémon Sprite and Image Dataset for Conditional Generation

[](https://github.com/ShanNicChi/pokemon-sprite-dataset#pok%C3%A9mon-sprite-and-image-dataset-for-conditional-generation)

This dataset contains sprites, animated sprites, Bulbapedia artworks, and tabular data for all of the Pokémon listed on Bulbapdia. We built this dataset to  [train a diffusion model](https://github.com/KyroChi/pokemon_sprite_generator)  to generate new Pokémon sprites.

This dataset is built on the back of the  [Bulbapeida](https://bulbapedia.bulbagarden.net/wiki/Main_Page)  and the  [PokéAPI](https://pokeapi.co/). It aggregates the resources required for building a generative diffusion model for Pokémon sprite animations.

Note that all of the sprites are owned by Nintendo, so use at your own risk!

Currently, there are three datasets:

-   Animated sprite gifs for all generation V Pokémon for shiny and normal Pokémon.
-   Unwrapped generation V sprites (i.e. each frame of the gif as an individual image)
-   A "full art" dataset, with the header images from Bulbapedia entries.

All three datasets have conditional and unconditional features available, which are scraped and stored in CSV format. Look at call signatures for the datasets to understand available options.

Below are examples from each of the three datasets:

-   Full Art:  [![](https://github.com/ShanNicChi/pokemon-sprite-dataset/raw/main/resorces/0001_Bulbasaur.png)](https://github.com/ShanNicChi/pokemon-sprite-dataset/blob/main/resorces/0001_Bulbasaur.png)
-   Generation V Sprites  [![](https://github.com/ShanNicChi/pokemon-sprite-dataset/raw/main/resorces/Spr_5b_001.gif)](https://github.com/ShanNicChi/pokemon-sprite-dataset/blob/main/resorces/Spr_5b_001.gif)
-   Unwrapped Generation V Sprites  [![](https://github.com/ShanNicChi/pokemon-sprite-dataset/raw/main/resorces/0.png)](https://github.com/ShanNicChi/pokemon-sprite-dataset/blob/main/resorces/0.png)

## Getting Started

[](https://github.com/ShanNicChi/pokemon-sprite-dataset#getting-started)

Clone the repository and then run

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

From here, you can look at  `example/`  to find Jupiter notebooks demonstrating the usage of the API.

Enjoy!
