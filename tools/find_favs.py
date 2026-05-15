import favorites
from Pokemon import Pokemon   # Optional but recommended

if __name__ == "__main__":
    # Load favorites data once
    favorites.getFavoritesDictionary()

    # Get full Pokemon objects
    bonsly = favorites.getPokemon("Bonsly")
    combee = favorites.getPokemon("Combee")

    if bonsly and combee:
        print(f"\nBonsly has {len(bonsly.favoriteItems)} unique favorite items")
        print(f"Combee has {len(combee.favoriteItems)} unique favorite items")

        # Test shared categories
        result = favorites.pokemon_share_category_items([bonsly, combee])
        print("\nDo they share at least one item per category?")
        for cat, has_shared in result.items():
            print(f"  {cat}: {'Yes' if has_shared else 'No'}")