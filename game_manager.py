from game import Game
from monster_manager import MonsterManager

class GameManager:

    def __init__(self):
        self.games = {}
        self.monsterMgr = MonsterManager()

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
            return []
        return []

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
        try:
            # TODO Be able to add user created characters to encounters
            if name in self.monsterMgr.monsters:
                #  or characterManager.characterExists(name) is True
                game = self.getActive()
                encounter = self.getActiveEncounter()
                self.games[game].encounters[encounter].monsters.append(name)
                return True
            else:
                print("Monster or NPC name not found")
                return False
        except:
            return False

    def getMonster(self, name):
        try:
            for monster in self.monsterMgr.monsters:
                if name in monster:
                    return self.monsterMgr.monsters[name]
        except:
            print("what")
            return False
