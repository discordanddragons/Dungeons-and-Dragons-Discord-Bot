# Character creation stuff
class characterManager:
    def __init__(self):
        self.characters = {}

    def characterExists(self, name):
        if name in self.characters:
            return True
        return False

    def addCharacter(self, name, owner):
        #False for already exists True for successfully created character
        if self.characterExists(name):
            return False
        self.characters[name] = Character(name,owner,False)
        return True

    def setActive(self, name, owner):
        if self.characterExists(name) and self.characters[name].owner == owner:
            for character in self.characters:
                if self.characters[character].owner == owner:
                    self.characters[character].active = False
            self.characters[name].active = True
            return True
        else:
            return False

    def getCharacters(self, owner):
        ownersCharacters = []
        for character in self.characters:
            if self.characters[character].owner == owner:
                ownersCharacters.append(character)
        return ownersCharacters


class Character:
    def __init__(self, name, owner, active=0):
        self.name = name
        self.owner = owner
        self.active = active
        self.stats = Stats()

class Stats:
    def __init__(self, stre=10, dex=10, con=10, inte=10, wis=10, cha=10):
        self.strength = stre
        self.dexterity = dex
        self.constitution = con
        self.intelligence = inte
        self.wisdom = wis
        self.charisma = cha

#class Skills:

#class Items:
