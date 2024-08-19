from poke_sprite_dataset.scrape.scraper import scrape_bulbapedia

if __name__ == "__main__":
    data_dir = input("Directory to save data to: ")
    scrape_bulbapedia({"save_path": data_dir})
