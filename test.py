from characterManager import *

characterName = "Froodo"
authorName = "Esteban"
gameName = "Lord Of The Rings"
gameName2 = "Kung Fu Hustle"
gameSize = 4


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


def UtilityTest():
    print("\nUtility Test Start")
    status = True
    utility = Utility()

    status &= test("Roll",utility.roll(1, 20) is None,False)
    status &= test("Flip",utility.flip() is None,False)
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



characterManagerTest()
UtilityTest()
gameTest()








