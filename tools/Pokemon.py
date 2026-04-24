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