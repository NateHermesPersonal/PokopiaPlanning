from collections import defaultdict
import csv
import re
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

REF_DIR = Path(__file__).parent.parent / "reference"
itemCategories = ["Decoration", "Toy", "Relaxation"]
itemCategoriesSet = set(itemCategories)
baseUrl = "https://www.serebii.net/pokemonpokopia/favorites/"
favoritesUrl = "https://www.serebii.net/pokemonpokopia/favorites.shtml"
favoritesDict = None

def get_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")

def get_all_favorite_categories():
    """Scrape the main page to get list of all favorite categories"""
    # print(f"Fetching all favorite categories from: {favoritesUrl}")
    soup = get_soup(favoritesUrl)
    
    categories = []
    
    for link in soup.find_all('a', href=True):
        href = link['href']
        name = link.get_text().strip()
        
        # Look for links pointing to favorite category pages
        if '/pokemonpokopia/favorites/' in href and href.endswith('.shtml') and name:
            # Extract clean name (e.g. "Strange stuff")
            category_name = name.strip()
            if category_name and category_name not in categories:
                categories.append(category_name)
    
    # print(f"Found {len(categories)} favorite categories.")
    return categories

def getFavoritesDictionary():
    global favoritesDict
    if favoritesDict is not None:
        # print("Favorites dictionary already set up!")
        return favoritesDict
    else:
        print("Building dictionary of favorite items")

    favoritesDict = defaultdict(list)
    favoritesCategories = get_all_favorite_categories()

    for category_page in favoritesCategories:
        short = category_page.replace(" ", "").lower()
        url = f"{baseUrl}{short}.shtml"
        # print(f"Scraping: {url}")
        
        soup = get_soup(url)
        items = []
        pending_item = None   # Holds the item until we find its category
        links = soup.find_all('a', href=True)

        for link in soup.find_all('a', href=True):
            name = link.get_text().strip()
            href = link['href']

            # Stop before the 'List of Pokémon' section
            if '/pokemonpokopia/pokedex/' in href.lower():
                # print("Reached Pokémon section, stopping.")
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
        # print(f"Found {len(unique_items)} '{category_page}' items:")
        favoritesDict[category_page] = unique_items
        # for item in unique_items:
        #     print(f"{item['Name']}  ({item['Category']})")

        # === Save to CSV (uncomment when ready) ===
        # csv_path = Path(f"{short}_items.csv")
        # with open(csv_path, "w", newline="", encoding="utf-8") as f:
        #     writer = csv.DictWriter(f, fieldnames=["Name", "Category"])
        #     writer.writeheader()
        #     writer.writerows(unique_items)
        # print(f"Saved to {csv_path}\n")

    # print(favoritesDict.keys())

    # print("Built Dictionary of Favorites items!")
    return favoritesDict

def getPokemon(pokemon_name: str):
    """Return a fully loaded Pokemon object"""
    with open(REF_DIR / 'Pokopia.csv', mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["Name"] == pokemon_name:
                print(f"Found {pokemon_name}!")
                from Pokemon import Pokemon          # Local import
                p = Pokemon(row)
                return p
                
    print(f"WARNING: '{pokemon_name}' not found in Pokopia.csv")
    return None


def getFavoriteItems(pokemon_name: str):
    """Convenience function: return only the list of favorite item names"""
    p = getPokemon(pokemon_name)
    if p:
        return p.favoriteItems
    return None

def pokemon_share_category_items(pokemon_list):
    """Check if a group of Pokemon share at least one item in each category"""
    if not pokemon_list:
        return {cat: False for cat in itemCategories}

    # Ensure all Pokemon have their favoriteItems loaded
    for p in pokemon_list:
        if not hasattr(p, 'favoriteItems') or len(p.favoriteItems) == 0:
            p.getFavoriteItems()

    category_items = {cat: [] for cat in itemCategories}

    fav_dict = getFavoritesDictionary()

    for p in pokemon_list:
        p_by_cat = defaultdict(list)
        for item_name in p.favoriteItems:
            for items_list in fav_dict.values():
                for item in items_list:
                    if item["Name"] == item_name:
                        cat = item.get("Category")
                        if cat in itemCategories:
                            p_by_cat[cat].append(item_name)
                        break

        for cat in itemCategories:
            category_items[cat].append(set(p_by_cat.get(cat, [])))

    # Compute shared items per category
    result = {}
    for cat in itemCategories:
        if not category_items[cat]:
            result[cat] = False
            continue
            
        common = category_items[cat][0].copy()
        for item_set in category_items[cat][1:]:
            common &= item_set
            if not common:
                break
        result[cat] = len(common) > 0

    return result

def get_common_favorite_items(pokemon_list):
    """
    Returns items that are common to ALL Pokemon in the list,
    grouped by category (no duplicates).
    """
    if len(pokemon_list) < 2:
        print("Need at least 2 Pokemon to find common items.")
        return {}

    # Ensure all Pokemon have their favoriteItems loaded
    for p in pokemon_list:
        if not hasattr(p, 'favoriteItems') or len(p.favoriteItems) == 0:
            p.getFavoriteItems()

    # Get items common to ALL Pokemon (unique names)
    item_sets = [set(p.favoriteItems) for p in pokemon_list]
    common_item_names = item_sets[0].copy()
    for s in item_sets[1:]:
        common_item_names &= s

    if not common_item_names:
        print("No items in common across all Pokemon.")
        return {}

    # Group common items by category - using a set to prevent duplicates
    from collections import defaultdict
    common_by_category = defaultdict(list)
    seen_in_output = set()          # Extra safety

    fav_dict = getFavoritesDictionary()

    for item_name in sorted(common_item_names):
        added = False
        for items_list in fav_dict.values():
            for item in items_list:
                if item["Name"] == item_name:
                    cat = item.get("Category", "None")
                    if cat in itemCategories and item_name not in seen_in_output:
                        common_by_category[cat].append(item_name)
                        seen_in_output.add(item_name)
                        added = True
                    break
            if added:
                break  # Stop once we've placed the item

    print(f"Found {len(common_item_names)} unique items common to all {len(pokemon_list)} Pokemon.")
    return dict(common_by_category)