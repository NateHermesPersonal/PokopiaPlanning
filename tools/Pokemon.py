from favorites import getFavoritesDictionary, itemCategories, itemCategoriesSet

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
        self.expandedFavorites = []
        seen = {}
        # Track which categories we've covered
        coveredCategories = set()
        for favCategory in self.favorites:
            if not favCategory or favCategory not in favDictionary:
                continue

            for item in favDictionary[favCategory]:
                itemName = item["Name"]
                itemCategory = item.get("Category", None)

                if itemName not in seen:
                    seen[itemName] = item
                    # self.favoriteItems.append(item)
                    self.favoriteItems.append(itemName) # just the name, or customize further?
                    # if not silent:
                    #     print(f"{itemName}({itemCategory})")
                    self.expandedFavorites.append(f"{itemName}({itemCategory})")
                    # Record that we have this category
                    if itemCategory in itemCategories:
                        coveredCategories.add(itemCategory)

        # Optional: Print warning if missing categories
        # missing = itemCategoriesSet - coveredCategories
        # if missing:
        #     print(f"Warning: {self.name} is missing items from categories: {missing}")
        # else:
        #     print(f"{self.name} has items from all categories: ({itemCategoriesSet})")

        # print(f"{self.name} → {len(self.favoriteItems)} unique favorite items")