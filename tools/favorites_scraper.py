import csv
import re
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

favoritesCategories = ["Strange stuff"]
baseUrl = "https://www.serebii.net/pokemonpokopia/favorites/"

def get_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")

def main():
    for category in favoritesCategories:
        short = category.replace(" ", "").lower()
        url = f"{baseUrl}{short}.shtml"
        print(f"Scraping: {url}")
        
        soup = get_soup(url)
        items = []

        for link in soup.find_all('a', href=True):
            name = link.get_text().strip()
            href = link['href']
            category = None

            # Better stopping condition - look for Pokémon links
            # if '/pokedex/' in href.lower():
            #     print("Reached Pokémon section, stopping.")
            #     break

            # Only keep actual item links
            if '/pokemonpokopia/items/' in href and name:
                # Skip the category links (Decoration, Toy, Relaxation)
                if name not in ["Decoration", "Toy", "Relaxation"]:
                    # print(f"Adding {name}")
                    items.append(f"{name} ({category})")
                else:
                    # print(f"skipping {name}")
                    category = name

        unique_items = list(dict.fromkeys(items))  # remove duplicates, keep order
        print(f"Found {len(unique_items)} items in {category}:")
        for item in unique_items:
        #     # print("  •", item)
            print(item)
        
        # Optional: save to CSV
        # with open(f"{short}_items.csv", "w", newline="", encoding="utf-8") as f:
        #     writer = csv.writer(f)
        #     writer.writerow(["Item Name"])
        #     writer.writerows([[item] for item in unique_items])
    
    print("All done!")


if __name__ == "__main__":
    main()