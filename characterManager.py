# Character creation stuff
from random import randint
from pprint import pprint
import re
import json


class characterManager:
    
    def __init__(self):
        self.characters = {}
        self.utility = Utility()
        self.raceMgr = racemanager()

    def characterExists(self, name):
        if name in self.characters:
            return True
        return False

    def addCharacter(self, name, owner):
        # False for already exists True for successfully created character
        if self.characterExists(name):
            return False
        self.characters[name] = Character(name, owner, False)
        print("Created", name)
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

    def getActive(self,owner):
        for character in self.characters:
            if self.characters[character].owner == owner:
                if self.characters[character].active == True:
                    return character
        return False
    
    def roll(self,owner,statType):
        character = self.getActive(owner)
        if character == False:
            return False
        else:
            diceType = 20
            output = character + " is rolling for "+statType + "\n"
            output += "Using a d"+str(20)+" "+character+" rolled a "+str(self.utility.roll(1,20))
            raceAbilities = self.raceMgr.races[self.getClass(owner)].abilities
            if statType in raceAbilities:
                if raceAbilities[statType] > 0:
                    output += "+"+str(raceAbilities[statType])+"(race)"
                else:
                    output += str(raceAbilities[statType])+"(race)"
            print(output)

    def getCharacters(self, owner):
        ownersCharacters = []
        for character in self.characters:
            if self.characters[character].owner == owner:
                ownersCharacters.append(character)
        return ownersCharacters

    def addSkill(self, characterName, skill):
        self.characters[characterName].skills.append(skill)

    def addItem(self, characterName, item):
        self.characters[characterName].items.append(item)

    def setLanguages(self, characterName, language):
        self.characters[characterName].languages.append(language)

    def getLanguages(self, characterName):
        knownLanguages = []
        for language in self.characters[characterName].languages:
            knownLanguages.append(language)
        return knownLanguages

    def getClass(self,owner):
        character = self.getActive(owner)
        if character == False:
            return False
        else:
            return self.characters[character].gofuckyourself["race"]

    def setRace(self,owner,raceName):
        character = self.getActive(owner)
        if character == False:
            return False
        else:
            if raceName in self.raceMgr.races:
                self.characters[character].gofuckyourself["race"] = raceName
                print("Your race is now: "+ raceName)
            else:
                print("pick a real race you dunce\n")
                print(", ".join(self.raceMgr.races))

    # sets values work on this logic to update anything not just stats
    def set(self, characterName, thing, value):
        statList = ["str", "strength", "dex", "dexterity", "int", "intelligence",
                    "con", "constitution", "wis", "wisdom", "cha", "charisma"]
        if thing in statList:
            self.characters[characterName].attributes.stats[thing] = value
            print("Setting stat:", thing, "to", value)
        # TODO add the ability to edit everything else
        else:
            self.characters[characterName].gofuckyourself[thing] = value
            print("set", thing, "to", value)

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
        self.attributes = Attributes()
        self.languages = []
        self.items = []
        self.skills = []
        self.builtUsing = ""
        self.gofuckyourself = {
            'maxHealth': 10,
            'currentHealth': 10,
            'characterClass': "Not Set",
            'level': 1,
            'race': "Not Set",
            'gold': 0,
            'description': "Not Set",
            'alignment': "Not Set"
        }


class Attributes:
    def __init__(self, stre=10, dex=10, con=10, inte=10, wis=10, cha=10):
        # Stats contain the characters base stats
        # modifier equation is round(stat - 10 / 2)
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

class racemanager:
    def __init__(self):
        #load json and add a class for each class
        self.races = {}
        with open('checkthisout.json') as f:
            data = json.load(f)
        for elem in data["race"]:
            abilities = {}
            languages = {}
            if "ability" in elem:
                abilities = elem["ability"]
            if "languageTags" in elem:
                languages = elem["languageTags"]
            self.races[elem["name"]] = raceStats(abilities,languages)
        #for key, value in self.classes.items():
        #    print(key,'\n')
        #    print(value)

class raceStats:
    def __init__(self,abilities,languages):
        self.abilities = abilities
        self.languages = languages
    def __str__(self):
        output = "abilities: "
        for key, value in self.abilities.items():
            output += key+":"+str(value)+", "
        output += "\nlanguages: " + ', '.join(self.languages) + "\n"
        return output
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






