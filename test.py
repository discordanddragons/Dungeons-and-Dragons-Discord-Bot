from characterManager import *

characterName = "Froodo"
authorName = "Esteban"
gameName = "Lord Of The Rings"
gameName2 = "Kung Fu Hustle"
gameSize = 4
encounterName = "Battle For Smaug"
encounterName2 = "Taco Rush"


def test(testName,condition,expectedValue = True):
    if condition == expectedValue:
        print("\t"+testName +": PASS")
        return True
    else:
        print(testName +": FAIL")
        return False


def characterManagerTest():
    print("\ncharacterManager Test Start")
    status = True
    manager = characterManager()
    #Test Character Adding
    status &= test("addCharacter",manager.addCharacter(characterName,authorName))
    status &= test("duplicate addCharacter",manager.addCharacter(characterName,authorName),False)

    #Test setActive
    status &= test("setActive",manager.setActive("Not in dict","Not in dict"),False)
    status &= test("getActive",manager.getActive(authorName),False)
    status &= test("setActive",manager.setActive(characterName,authorName))
    status &= test("getActive",manager.getActive(authorName),characterName)

    test("characterManager Test",status)

def raceManagerTest():
    raceMgr = raceManager()
    print("\nracemanager Test Start")
    status  = True
    status &= test("load races",len(raceMgr.races) > 0)
    test("raceManager Test",status)

def classManagerTest():
    classMgr = classManager()
    print("\nclassManager Test Start")
    status  = True
    status &= test("load classes",len(classMgr.classes) > 0)
    print(classMgr)
    test("classManager Test",status)


def UtilityTest():
    print("\nUtility Test Start")
    status = True

    status &= test("Roll",roll(1, 20) is None,False)
    status &= test("Flip",flip() is None,False)
    test("Utility Test",status)

     #Test setRace
    # manager.setRace(authorName,"Minotaur")
    # manager.roll(authorName,"str")


def gameTest():
    print("\nTesting Game creation commands")
    status = True
    game = gameManager()
    print("New Game Creation")
    status &= test("New Game", game.addGame(gameName, gameSize))
    status &= test("setActive", game.setActive(gameName))
    status &= test("get active games", game.getActive(), gameName)
    status &= test("New Game 2", game.addGame(gameName2, gameSize))
    status &= test("setActive when game is already active", game.setActive(gameName2), False)
    status &= test("Deactiveate Game", game.deActive())
    status &= test("setActive game 2", game.setActive(gameName2))
    status &= test("getActive", game.getActive(), gameName2)
    print("\nAdd/Delete Players")
    for i in range(1, 6):
        playerName = "player " + str(i)
        characterName = "character " + str(i)
        testName = "Add" + playerName
        if i == 5:
            status &= test("Player 5 should not be added", game.addPlayer(playerName, characterName), False)
        else:
            status &= test(testName, game.addPlayer(playerName, characterName))
    status &= test("Deleting Player 1 from game", game.deletePlayer("player 1"))
    status &= test("Get all games", len(game.getGames()) > 0)
    print(game)

def encounterTest():
    print("\nTesting Encounter creation commands")
    status = True
    game = gameManager()
    print("New Game Creation")
    status &= test("New Game", game.addGame(gameName, gameSize))
    status &= test("setActive", game.setActive(gameName))
    print("\nNew Encounter Creation")

    status &= test("New Encounter", game.addEncounter(encounterName))
    status &= test("setActive Encounter", game.setActiveEncounter(encounterName))
    status &= test("get active Encounter", game.getActiveEncounter(), encounterName)
    status &= test("New Encounter 2", game.addEncounter(encounterName2))
    status &= test("setActive when Encounter is already active", game.setActiveEncounter(encounterName2), False)
    status &= test("Deactiveate Encounter", game.deActiveEncounter())
    status &= test("setActive Encounter 2", game.setActiveEncounter(encounterName2))
    status &= test("getActive", game.getActiveEncounter(), encounterName2)
    status &= test("Add snek to active game", game.addMonster("snek"))
    status &= test("Get all encounters", len(game.getEncounters()) > 0)
    print("\n")
    print(game)

def monsterManagerTest():
    print("\nTesting Monsters")
    status = True
    monster = monsterManager()
    # status &= test("New Game", game.addGame(gameName, gameSize))
    print(monster)


#characterManagerTest()
#UtilityTest()
#gameTest()
#raceManagerTest()
#classManagerTest()
#encounterTest()
monsterManagerTest()






