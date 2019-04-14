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
        if owner in self.characters:
            ownerCharacters = self.characters[owner]
            if name in ownerCharacters:
                return False
            else:
                self.characters[owner][name] = Character(name, owner, False)
                return True
        else:
            self.characters[owner] = {}
            self.characters[owner][name] = Character(name, owner, False)
            return True

    def setActive(self, name, owner):
        try:
            for character in self.characters[owner]:
                self.characters[owner][character].active = False
            self.characters[owner][name].active = True
            return True
        except:
            return False

    def getActive(self, owner):
        try:
            for character in self.characters[owner]:
                if self.characters[owner][character].active == True:
                    return character
            return False
        except:
            return False

    def roll(self, owner, statType):
        character = self.getActive(owner)
        if character == False:
            return False
        else:
            diceType = 20
            output = character + " is rolling for " + statType + "\n"
            output += "Using a d" + str(20) + " " + character + " rolled a " + str(self.utility.roll(1, 20))
            raceAbilities = self.raceMgr.races[self.getRace(owner)].abilities
            if statType in raceAbilities:
                if raceAbilities[statType] > 0:
                    output += "+" + str(raceAbilities[statType]) + "(race)"
                else:
                    output += str(raceAbilities[statType]) + "(race)"
            print(output)

    def getCharacters(self, owner):
        try:
            print("getting the character")
            print(self.characters[owner])
            characters = []
            for key, value in self.characters[owner].items():
                print(value)
                characters.append(str(value))
            return characters
        except:
            return []

    def addSkill(self, owner, skill):
        character = self.getActive(owner)
        self.characters[owner][character].skills.append(skill)

    def addItem(self, owner, item):
        character = self.getActive(owner)
        self.characters[owner][character].items.append(item)

    def setLanguages(self, owner, language):
        character = self.getActive(owner)
        self.characters[owner][character].languages.append(language)

    def getLanguages(self, owner):
        character = self.getActive(owner)
        knownLanguages = []
        for language in self.characters[owner][character].languages:
            knownLanguages.append(language)
        return knownLanguages

    def getRace(self, owner):
        character = self.getActive(owner)
        if character == False:
            return False
        else:
            return self.characters[owner][character].gofuckyourself["race"]

    def setRace(self, owner, raceName):
        character = self.getActive(owner)
        if character == False:
            return False
        else:
            if raceName in self.raceMgr.races:
                self.characters[owner][character].gofuckyourself["race"] = raceName
                print("Your race is now: " + raceName)
            else:
                print("pick a real race you dunce\n")
                print(", ".join(self.raceMgr.races))

    # sets values work on this logic to update anything not just stats
    def set(self, owner, thing, value):
        character = self.getActive(owner)
        statList = ["str", "strength", "dex", "dexterity", "int", "intelligence",
                    "con", "constitution", "wis", "wisdom", "cha", "charisma"]
        if thing in statList:
            self.characters[owner][character].attributes.stats[thing] = value
            print("Setting stat:", thing, "to", value)
        # TODO add the ability to edit everything else
        else:
            self.characters[owner][character].gofuckyourself[thing] = value
            print("set", thing, "to", value)

    def setRandomStats(self, owner):
        character = self.getActive(owner)
        # sets the attributes to random values
        # Roll method of generating dnd character
        # Roll 4 6 sided dice and keep the top 3 then set the value to a stat
        for stat in self.characters[owner][character].attributes.stats:
            # print(stat)
            rolls = self.utility.roll(4, 6)
            # print("These are the random roll numbers", rolls)
            rolls.remove(min(rolls))
            # print("These are the random roll numbers after removing the lowest one", rolls)
            total = sum(rolls)
            # print(total)
            self.set(owner, stat, total)

    def getStats(self, owner):
        character = self.getActive(owner)
        return self.characters[owner][character].attributes.stats


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

    def __str__(self):
        output = "Character Name: " + self.name + "\n"
        output += "Class: " + self.gofuckyourself["characterClass"] + "\n"
        output += "Level: " + str(self.gofuckyourself["level"]) + "\n"
        output += "Health: " + str(self.gofuckyourself["currentHealth"]) + \
                  "/" + str(self.gofuckyourself["maxHealth"]) + "\n"
        output += "Race: " + self.gofuckyourself["race"] + "\n"
        output += "Gold: " + str(self.gofuckyourself["gold"]) + "\n"
        output += "Attributes: \n" + str(self.attributes)
        return output


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

    def __str__(self):
        output = ""
        for elem in self.stats:
            output += elem + ": " + str(self.stats[elem]) + "\n"
        return output


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

        # classes all have starting equipment
        self.equipment = []


class racemanager:
    def __init__(self):
        # load json and add a class for each class
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
            self.races[elem["name"]] = raceStats(abilities, languages)
        # for key, value in self.classes.items():
        #    print(key,'\n')
        #    print(value)


class raceStats:
    def __init__(self, abilities, languages):
        self.abilities = abilities
        self.languages = languages

    def __str__(self):
        output = "abilities: "
        for key, value in self.abilities.items():
            output += key + ":" + str(value) + ", "
        output += "\nlanguages: " + ', '.join(self.languages) + "\n"
        return output


# class Skills:

# class Items:


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





