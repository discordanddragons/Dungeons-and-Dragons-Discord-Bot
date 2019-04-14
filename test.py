from characterManager import characterManager

from characterManager import racemanager
from characterManager import Utility
characterName = "Gimli"
authorName = "Esteban"

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


characterManagerTest()
UtilityTest()