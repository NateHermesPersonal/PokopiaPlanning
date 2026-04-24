
import csv
import Pokemon

pokemon = []
categories = ["Blocky stuff","Glass stuff","Luxury","Strange stuff","Watching stuff"]
with open('Pokopia.csv', mode='r', newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        # print(row["Name"])
        p = Pokemon.Pokemon(row)
        # print(f"Adding {p.name} ({p.dexNum}) ({p.specialties}) ({p.favorites})")
        pokemon.append(p)
        if "Trade" in p.specialties:
            print(p.name)

# print(f"\n{len(pokemon)} total Pokemon")
# print(f"Each Pokemon has {Pokemon.Pokemon.numfavorites} favorites")