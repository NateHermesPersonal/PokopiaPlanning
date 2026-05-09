import csv
import re
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

favoritesCategories = ["Strange stuff"]
itemCategories = ["Decoration", "Toy", "Relaxation"]
baseUrl = "https://www.serebii.net/pokemonpokopia/favorites/"

def get_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")

def main():
    for category_page in favoritesCategories:
        short = category_page.replace(" ", "").lower()
        url = f"{baseUrl}{short}.shtml"
        print(f"Scraping: {url}")
        
        soup = get_soup(url)
        items = []
        pending_item = None   # Holds the item until we find its category
        links = soup.find_all('a', href=True)

        for link in soup.find_all('a', href=True):
            name = link.get_text().strip()
            href = link['href']

            # Stop before the 'List of Pokémon' section
            if '/pokemonpokopia/pokedex/' in href.lower():
                print("Reached Pokémon section, stopping.")
                break

            # === If we found a Category link ===
            if name in itemCategories:
                if pending_item:
                    pending_item["Category"] = name
                    items.append(pending_item)
                    pending_item = None
                continue

            # === If we found an Item link ===
            if '/pokemonpokopia/items/' in href and name and name not in itemCategories:
                # Save the previous pending item (in case it had no category)
                if pending_item:
                    items.append(pending_item)
                
                # Start tracking the new item
                pending_item = {
                    "Name": name,
                    "Category": "None"
                }

        # Add the very last item if it exists
        if pending_item:
            items.append(pending_item)

        # Remove duplicates while preserving order
        seen = {}
        unique_items = []
        for item in items:
            if item["Name"] not in seen:
                seen[item["Name"]] = True
                unique_items.append(item)

        # Print results
        print(f"Found {len(unique_items)} '{category_page}' items:")
        for item in unique_items:
            print(f"{item['Name']}  ({item['Category']})")

        # === Save to CSV (uncomment when ready) ===
        # csv_path = Path(f"{short}_items.csv")
        # with open(csv_path, "w", newline="", encoding="utf-8") as f:
        #     writer = csv.DictWriter(f, fieldnames=["Name", "Category"])
        #     writer.writeheader()
        #     writer.writerows(unique_items)
        # print(f"Saved to {csv_path}\n")

    print("All done!")

if __name__ == "__main__":
    main()