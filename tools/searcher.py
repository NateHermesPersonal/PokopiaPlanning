
import csv
import Pokemon

pokemon = []
categories = ["Blocky stuff","Glass stuff","Luxury","Strange stuff","Watching stuff"] # Wall Mirror
with open('Pokopia.csv', mode='r', newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        # print(row["Name"])
        p = Pokemon.Pokemon(row)
        # print(f"Adding {p.name} ({p.dexNum}) ({p.specialties}) ({p.favorites})")
        if "Trade" in p.specialties:
            # print(p.name)
            for c in categories:
                if c in p.favorites:
                    print(f"{p.name} ({c})")
                    pokemon.append(p)
                    break
            # else:
            #     print(f"{p.name} doesn't have a favorite of any of the categories")
print(f"{len(pokemon)} total compatible traders")

# print(f"\n{len(pokemon)} total Pokemon")
# print(f"Each Pokemon has {Pokemon.Pokemon.numfavorites} favorites")