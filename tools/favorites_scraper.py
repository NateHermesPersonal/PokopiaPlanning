import csv
import re
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

favoritesCategories = ["Strange stuff"]
baseUrl = "https://www.serebii.net/pokemonpokopia/favorites/"

def get_soup(url):
    """Fetches a URL and returns a BeautifulSoup object."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")

def main():
    for category in favoritesCategories:
        short = category.replace(" ", "").lower()
        url = f"{baseUrl}{short}.shtml"
        soup = get_soup(url)
        h1 = soup.find("h1")
        if not h1:
            print(f"  WARNING: No <h1> found on {url}")
            return None
        
        headerString = f"List of {category} Items "
        # stats_header = soup.find("h2", string=headerString)
        table = soup.find("table")
        # if not stats_header:
        #     print(f"  WARNING: Could not find '{headerString}' on {url}")
    
        print("done")


if __name__ == "__main__":
    main()