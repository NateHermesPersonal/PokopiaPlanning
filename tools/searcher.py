
import csv
import Pokemon

pokemon = []
with open('Pokopia.csv', mode='r', newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        # print(row["Name"])
        p = Pokemon.Pokemon(row["Name"],row["Number"])
        print(f"Adding {p.name} ({p.dexNum})")
        pokemon.append(p)

print(f"\n{len(pokemon)} total Pokemon")