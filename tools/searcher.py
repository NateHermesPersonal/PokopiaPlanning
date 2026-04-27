
import csv
import Pokemon

pokemon = []
categories = ["Blocky stuff","Glass stuff","Luxury","Strange stuff","Watching stuff"] # Wall Mirror
habitats = {}
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
                    h = p.habitat
                    if h not in habitats.keys():
                        habitats[h] = 1
                    else:
                        habitats[h] += 1
                    print(f"{p.name}[{h}] ({c})")
                    pokemon.append(p)
                    break
            # else:
            #     print(f"{p.name} doesn't have a favorite of any of the categories")
print(f"{len(pokemon)} total compatible traders")
print(habitats)

# print(f"\n{len(pokemon)} total Pokemon")
# print(f"Each Pokemon has {Pokemon.Pokemon.numfavorites} favorites")