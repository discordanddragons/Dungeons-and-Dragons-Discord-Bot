
from characterManager import characterManager
from characterManager import roll
from characterManager import flip

from characterManager import raceManager
from characterManager import classManager
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


characterManagerTest()
UtilityTest()
raceManagerTest()
classManagerTest()