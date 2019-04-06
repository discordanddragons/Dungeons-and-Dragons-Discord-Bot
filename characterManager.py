# Character creation stuff
from random import randint
import re


class characterManager:
    def __init__(self):
        self.characters = {}
        self.utility = Utility()

    def characterExists(self, name):
        if name in self.characters:
            return True
        return False

    def addCharacter(self, name, owner):
        # False for already exists True for successfully created character
        if self.characterExists(name):
            return False
        self.characters[name] = Character(name, owner, False)
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

    def getLanguages(self, characterName):
        knownLanguages = []
        for language in self.characters[characterName].languages:
            knownLanguages.append(language)
        return knownLanguages

    def setLanguages(self, characterName, language):
        self.characters[characterName].languages.append(language)

    # sets values work on this logic to update anything not just stats
    def set(self, characterName, stat, value):
        self.characters[characterName].attributes.stats[stat] = value
        print("set", stat, "to", value)

    def setRandomStats(self, characterName):
        #sets the attributes to random values
        # Roll method of generating dnd character
        # Roll 4 6 sided dice and keep the top 3 then set the value to a stat
        for stat in self.characters[characterName].attributes.stats:
            # print(stat)
            rolls = self.utility.roll(4, 6)
            # print("These are the random roll numbers", rolls)
            rolls.remove(min(rolls))
            # print("These are the random roll numbers after removing the lowest one", rolls)
            total = sum(rolls)
            # print(total)
            self.set(characterName, stat, total)

    def getStats(self, characterName):
        return self.characters[characterName].attributes.stats

class Character:
    def __init__(self, name, owner, active):
        self.name = name
        self.owner = owner
        self.active = active
        self.builtUsing = ""
        self.attributes = Attributes()
        self.maxHealth = 10
        self.currentHealth = 10
        self.characterClass = "Not Set"
        self.level = 1
        self.race = "Not Set"
        self.gold = 0
        self.description = "Not Set"
        self.alignment = "Not Set"
        self.languages = []
        self.items = []
        self.skills = []


class Attributes:
    def __init__(self, stre=10, dex=10, con=10, inte=10, wis=10, cha=10):
        # Stats contain the characters base stats
        self.stats = {
            'strength': stre,
            'dexterity': dex,
            'constitution': con,
            'intelligence': inte,
            'wisdom': wis,
            'charisma': cha
        }
        # modifiers contain the stat modifiers that could come from:
        #   Class Bonus
        #   Race Bonus
        #   Abilities
        self.modifiers = {
            'strength': 0,
            'dexterity': 0,
            'constitution': 0,
            'intelligence': 0,
            'wisdom': 0,
            'charisma': 0
        }
        self.utility = Utility()
        self.characterManager = characterManager()


class CharacterClass:
    def __init__(self):
        self.hitPoints = {
            'hitDice': '',
            'lvl1hitPoints': '',
            'nextLevelHitPoints': ''
        }

        self.proficiencies = {
            'armor': [],
            'weapons': [],
            'tools': [],
            'savingThrows': [],
            'skills': []
        }

        # Each class gains features every level and increased proficiency
        self.features = {
        }

        #classes all have starting equipment
        self.equipment = []



#class Skills:

#class Items:


class Utility:
    def roll(self, numberOfRolls, sidesOfDice):
        rolls = []
        # Takes in a message in the form of: !roll 4d6
        if numberOfRolls < 100:
            for n in range(numberOfRolls):
                temp = randint(1, sidesOfDice)
                rolls.append(temp)
                # print(temp)
        return rolls

    def flip(self):
        temp = randint(0, 1)
        if temp is 0:
            return "Heads"
        else:
            return "Tails"






