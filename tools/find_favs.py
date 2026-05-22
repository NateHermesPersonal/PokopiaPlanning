import favorites
from Pokemon import Pokemon   # Optional but recommended

if __name__ == "__main__":
    # Load favorites data once
    favorites.getFavoritesDictionary()

    # Get full Pokemon objects
    # pokemonNames = ["Zapdos"]
    pokemonNames = ["Bonsly","Combee","Dartrix","Elekid","Pik"] # include bogus name to ensure proper handling
    pokemonObjects: list[Pokemon] = [
        p for name in pokemonNames 
        if (p := favorites.getPokemon(name)) is not None
    ]

    for pokemon in pokemonObjects:
        print(f"{pokemon.name} has {len(pokemon.favoriteItems)} unique favorite items")
        # print(pokemon.favoriteItems)
    
    # Check for common habitat
    if pokemonObjects:
        nameString = ",".join([f"{p.name}" for p in pokemonObjects])
        print(f"\nLooking at Pokemon {nameString}:")

        first_habitat = pokemonObjects[0].habitat
        all_same = all(p.habitat == first_habitat for p in pokemonObjects)
        
        if all_same:
            print(f"\nAll Pokémon have the same ideal habitat: {first_habitat}")
        else:
            habitats = {p.habitat for p in pokemonObjects}
            habitatString = ",".join([f"{p.name}({p.habitat})" for p in pokemonObjects])
            print(f"\nWARNING: Mixed ideal habitats: {habitatString}")
        
        # Test shared favorites categories
        result = favorites.pokemon_share_category_items(pokemonObjects)
        print(f"\nDo they share at least one item per category?")
        for cat, has_shared in result.items():
            print(f"  {cat}: {'Yes' if has_shared else 'No'}")
        
        # See which favorite items they have in common
        print("\nItems in common:")
        common = favorites.get_common_favorite_items(pokemonObjects)
        for cat, items in common.items():
            print(f"  {cat}: {items} ({len(items)})")

    items = ["Wall mirror"]
    for item in items:
        favs: list[Pokemon] = favorites.get_pokemon_that_like_item(item, return_objects=True)
        matches = [f"{p.name} ({p.habitat})" for p in favs if "Trade" in p.specialties]
        nameString = ",".join(matches)
        print(f"The following {len(matches)} Pokemon like {item}: {nameString}")