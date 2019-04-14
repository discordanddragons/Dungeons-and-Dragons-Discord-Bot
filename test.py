from characterManager import characterManager

from characterManager import racemanager
characterName = "Gimli"
authorName = "Esteban"

def estebanTests():
    manager = characterManager()
    #Test Character Adding
    if manager.addCharacter(characterName,authorName):
        print("addCharacter: PASS")
    else:
        print("addCharacter: FAIL")

    if not manager.addCharacter(characterName,authorName):
        print("duplicate addCharacter: PASS")
    else:
        print("duplicate addCharacter: FAIL")

    #Test setActive
    if not manager.setActive("Not in dict","Not in dict"):
        print("setActive: PASS")
    else:
        print("setActive: FAIL")

    if manager.getActive(authorName) == False:
        print("getActive: Pass")
    else:
        print("getActive: FAIL")

    if manager.setActive(characterName,authorName):
        print("setActive: PASS")
    else:
        print("setActive: FAIL")

    if manager.getActive(authorName) == characterName:
        print("getActive: Pass")
    else:
        print("getActive: FAIL")

    #Utility Tests
    if manager.utility.roll(1, 20) is None:
        print("Roll: FAIL")
    else:
        print("Roll: Pass")

    if manager.utility.flip() is None:
        print("flip: FAIL")
    else:
        print("flip: Pass")

     #Test setRace
    # manager.setRace(authorName,"Minotaur")
    # manager.roll(authorName,"str")


estebanTests()
