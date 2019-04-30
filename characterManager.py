# Character creation stuff
from random import randint
from pprint import pprint
import re
import json


class gameManager:

    def __init__(self):
        self.games = {}

    def __str__(self):
        output = ""
        for elem in self.games:
            output += elem + ": \n"
            output += str(self.games[elem])
        return output

    def addGame(self, name, size):
        if name in self.games:
            return False
        else:
            self.games[name] = Game(name, size, False)
            return True

    def setActive(self, gameName):
        try:
            for game in self.games:
                # if any of the games are currently active, don't let the DM set another active game.
                if self.games[game].active is True:
                    return False
                else:
                    self.games[gameName].active = True
                    return True
        except:
            return False

    def getActive(self):
        try:
            for game in self.games:
                if self.games[game].active is True:
                    return game
        except:
            return False

    def deActive(self):
        try:
            for game in self.games:
                if self.games[game].active is True:
                    self.games[game].active = False
                    return True
        except:
            return False

    def addPlayer(self, playerName, activeCharacterName):
        try:
            game = self.getActive()
            if len(self.games[game].players) < self.games[game].size:
                self.games[game].players[playerName] = activeCharacterName
                return True
            else:
                return False
        except:
            return False

    def deletePlayer(self, playerName):
        try:
            game = self.getActive()
            self.games[game].players.pop(playerName, None)
            return True
        except:
            return False

    def getGames(self):
        try:
            gameList = []
            for game in self.games:
                gameList.append(game)
                return gameList
        except:
            return False

    def getPlayers(self):
        try:
            game = self.getActive()
            return self.games[game].players
        except:
            return False

    def addEncounter(self, name):
        try:
            game = self.getActive()
            if name in self.games[game].encounters:
                return False
            else:
                self.games[game].encounters[name] = Encounter(name, False)
                return True
        except:
            return False

    def getEncounters(self):
        try:
            game = self.getActive()
            encounterList = []
            for encounter in self.games[game].encounters:
                encounterList.append(encounter)
                return encounterList
        except:
            return False

    def setActiveEncounter(self, encounterName):
        try:
            game = self.getActive()
            for encounter in self.games[game].encounters:
                if self.games[game].encounters[encounter].active is True:
                    return False
                else:
                    self.games[game].encounters[encounterName].active = True
                    return True
        except:
            return False

    def getActiveEncounter(self):
        try:
            game = self.getActive()
            for encounter in self.games[game].encounters:
                if self.games[game].encounters[encounter].active is True:
                    return encounter
        except:
            return False

    def deActiveEncounter(self):
        try:
            game = self.getActive()
            encounter = self.getActiveEncounter()
            self.games[game].encounters[encounter].active = False
            return True
        except:
            return False

    def addMonster(self, name):
        monsterList = ["snek"]
        npcList = ["bob"]
        try:
            game = self.getActive()
            encounter = self.getActiveEncounter()
            if name in monsterList or name in npcList:
                self.games[game].encounters[encounter].monsters.append(name)
                return True
            else:
                return False
        except:
            return False


class Game:
    def __init__(self, name, size, active):
        self.name = name
        self.active = active
        self.size = size
        self.description = ""
        self.players = {}
        self.encounters = {}

    def __str__(self):
        output = ""
        output += "Name: " + self.name + "\n"
        output += "Active: " + str(self.active) + "\n"
        output += "Size: " + str(self.size) + "\n"
        for player in self.players:
            output += player + ": " + str(self.players[player]) + "\n"
        for encounter in self.encounters:
            output += encounter+": "+str(self.encounters[encounter])+"\n"
        return output


class Encounter:
    def __init__(self, name, active):
        self.name = name
        self.active = active
        self.monsters = []

    def __str__(self):
        output = ""
        output += "Name: " + self.name + "\n"
        output += "Active: " + str(self.active) + "\n"
        for elem in self.monsters:
            output += "Monsters: " + elem
        return output


class monsterManager:
    def __init__(self):
        # load json and add a class for each class
        self.monsters = {}
        with open('./json/monsters.json', encoding="utf8") as f:
            data = json.load(f)
        for monster in self.monsters:
            name = ""
            if "name" in monster:
                name = monster["name"]
            self.monsters[monster["name"]] = monster(name)

    def __str__(self):
        output = ""
        for elem in self.monsters:
            output += elem + ": \n"
            output += str(self.monsters[elem])
        return output


class monster:
    def __init__(self, name):
        self.name = name
        self.meta = ""
        self.ac = ""
        self.hp = ""
        self.speed = ""

    def __str__(self):
        output = ""
        for elem in self.monsters:
            output += elem + ": \n"
            output += str(self.monsters[elem])
        return output


class characterManager:

    def __init__(self):
        self.characters = {}
        self.raceMgr = raceManager()

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

    def getActive(self,owner):
        try:
            for character in self.characters[owner]:
                if self.characters[owner][character].active == True:
                    return character
            return False
        except:
            return False

    def roll(self,owner,statType):
        character = self.getActive(owner)
        if character == False:
            return False
        else:
            diceType = 20

            output = character + " is rolling for "+statType + "\n"
            output += "Using a d"+str(20)+" "+character+" rolled a "+str(roll(1,20))
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

            for key,value in self.characters[owner].items():
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

    def getRace(self,owner):
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

                print("Your race is now: "+ raceName)
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
        #sets the attributes to random values
        # Roll method of generating dnd character
        # Roll 4 6 sided dice and keep the top 3 then set the value to a stat
        for stat in self.characters[owner][character].attributes.stats:
            # print(stat)
            rolls = roll(4, 6)
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
    def levelup(self):
        self.gofuckyourself.level += 1
        maxHealth += roll(1,8)

    def __str__(self):
        output = "Character Name: " + self.name + "\n"
        output += "Class: " + self.gofuckyourself["characterClass"] + "\n"
        output += "Level: " + str(self.gofuckyourself["level"]) + "\n"
        output += "Health: " + str(self.gofuckyourself["currentHealth"]) + \
                    "/" + str(self.gofuckyourself["maxHealth"]) + "\n"
        output += "Race: " + self.gofuckyourself["race"] + "\n"
        output += "Gold: " + str(self.gofuckyourself["gold"]) + "\n"
        output += "Attributes: \n"+ str(self.attributes)
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
            output += elem+": "+str(self.stats[elem])+"\n"
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


class raceManager:
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


class classManager:
    def __init__(self):
        # load json and add a class for each class
        self.classes = {}
        with open('./json/classes.json', encoding="utf8") as f:
            data = json.load(f)
        for elem in data:
            hitPoints = None
            Proficiencies = None
            Equipment = None
            if "Class Features" in data[elem]:
                classFeatures = data[elem]["Class Features"]
                if "Hit Points" in classFeatures:
                    hitPoints =classFeatures["Hit Points"]["content"]
                    if len(hitPoints) is 3:
                        hitDie = ""
                        regex = r"\d+d\d+"
                        matches = re.search(regex, hitPoints[0])
                        if matches:
                            hitDie = matches.group()
                    else:
                        print(elem+" does not match expected json structure for hit points")
                if "Proficiencies" in classFeatures:
                    proficiencies =classFeatures["Proficiencies"]["content"]
                    output = ""
                    for proficiency in proficiencies:
                        output += " "+proficiency
 
                    regex = r"(?<=\*\*).{1,14}(?=:\*\*)"
                    matches = re.finditer(regex, output, re.MULTILINE)
                    start = 0
                    end = 0
                    name = ""
                    values = []
                    proficiencies = {}
                    for match in matches:
                        if start == 0:
                            start = match.span()[1]+3
                        else:
                            name = output[end:start-3].lstrip()[2:]
                            end = match.span()[0] -2
                            values = output[start:end].lstrip()
                            values = values.split(",")
                            start = match.span()[1]+3
                            proficiencies[name] = values
                    name = output[end:start-3].lstrip()[2:]
                    values = output[start:].lstrip()
                    values = values.split(",")
                    proficiencies[name] = values
                self.classes[elem] = classStats(hitDie, "common",proficiencies)
    def __str__(self):
        output = ""
        for elem in self.classes:
            output += elem + ": \n"
            output += str(self.classes[elem])
        return output
        # for key, value in self.classes.items():
        #    print(key,'\n')
        #    print(value)

class classStats:
    def __init__(self, hitDice, languages,proficiencies):
        self.hitDice = hitDice
        self.proficiencies = proficiencies
        self.languages = languages

    def __str__(self):
        output = "hit dice: "+ self.hitDice+"\n"
        output += "Proficiencies:\n"
        for elem in self.proficiencies:
            output += "\t"+elem+": "+str(self.proficiencies[elem])+"\n"
        return output
# class Skills:

# class Items:


def roll(numberOfRolls, sidesOfDice):
    rolls = []
    # Takes in a message in the form of: !roll 4d6
    if numberOfRolls < 100:
        for n in range(numberOfRolls):
            temp = randint(1, sidesOfDice)
            rolls.append(temp)
            # print(temp)
    return rolls

def flip():
    temp = randint(0, 1)
    if temp is 0:
        return "Heads"
    else:
        return "Tails"





