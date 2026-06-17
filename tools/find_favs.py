from datetime import datetime

import favorites
from Pokemon import Pokemon   # Optional but recommended

if __name__ == "__main__":
    # Load favorites data once
    favorites.getFavoritesDictionary()

    # Get full Pokemon objects
    # pokemonNames = ["Zapdos"]
    # pokemonNames = ["Bonsly","Combee","Dartrix","Elekid","Pik"] # include bogus name to ensure proper handling
    
    # pokemonNames = ["Larvitar"]
    # pokemonNames = ["Haxorus","Axew","Duskull"]
    # pokemonNames = ["Mareep","Combee","Venusaur","Ariados","Bastiodon","Cacturne"]
    # pokemonNames = ["Paldean Wooper","Trapinch","Girafarig","Rolycoly","Torkoal"]
    pokemonNames = ["Girafarig","Rolycoly","Torkoal"]
    pokemonObjects: list[Pokemon] = [
        p for name in pokemonNames 
        if (p := favorites.getPokemon(name)) is not None
    ]

    for pokemon in pokemonObjects:
        print(f"{pokemon.name} has {len(pokemon.favoriteItems)} unique favorite items")
        timestamp = datetime.now().strftime("%m%d%y_%H%M%S")
        filename = f"output/{pokemon.name}_favorites_{timestamp}.txt"
        with open(filename, mode='w') as file:
            file.write('\n'.join(pokemon.expandedFavorites))
            print(f"Saved {pokemon.name}'s favorite items to {filename}")
    
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
        timestamp = datetime.now().strftime("%m%d%y_%H%M%S")
        filename = f"output/{nameString}_shared_favorites_{timestamp}.txt"
        with open(filename, mode='w') as file:
            for cat in common.keys():
                for item in common[cat]:
                    file.write(f"{item}({cat})\n")
            print(f"Shared favorites of {nameString} saved to {filename}")
        
    # palletteResidents = favorites.getZoneResidents(5)
    # residentNameString = f"{",".join([p.name for p in palletteResidents])} ({len(palletteResidents)})"
    # print(f"{residentNameString=}")

    #  for "trade market"
    # items = ["Wall mirror"]
    # for item in items:
    #     favs: list[Pokemon] = favorites.get_pokemon_that_like_item(item, return_objects=True)
    #     matches = [f"{p.name} ({p.habitat})" for p in favs if "Trade" in p.specialties]
    #     nameString = ",".join(matches)
    #     print(f"The following {len(matches)} Pokemon like {item}: {nameString}")