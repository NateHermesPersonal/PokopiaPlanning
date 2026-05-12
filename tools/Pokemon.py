from favorites import getFavoritesDictionary

class Pokemon:
    numspecialties = 2
    numfavorites = 6

    def __init__(self, data):
        self.name = data['Name']
        self.dexNum = data['Number']
        self.habitat = data["Ideal Habitat"]
        self.specialties = []
        for s in range(self.numspecialties):
            self.specialties.append(data[f"Specialty {s+1}"])
        self.favorites = []
        for f in range(self.numfavorites):
            self.favorites.append(data[f"Favorite {f+1}"])
        self.getFavoriteItems()

    def getFavoriteItems(self):
        favDictionary = getFavoritesDictionary()
        self.favoriteItems = []
        seen = {}
        for favCategory in self.favorites:
            for item in favDictionary.get(favCategory, []):
                itemName = item["Name"]
                if itemName not in seen:
                    seen[itemName] = item
                    # self.favoriteItems.append(item)
                    self.favoriteItems.append(itemName) # just the name, or customize further?
        # print(f"Found {len(self.favoriteItems)} favorite items")