from characterManager import characterManager

from characterManager import racemanager

def estebanTests():
    manager = characterManager()
    #Test Character Adding
    if manager.addCharacter("playerName","discordName"):
        print("addCharacter: PASS")
    else:
        print("addCharacter: FAIL")

    if not manager.addCharacter("playerName","discordName"):
        print("duplicate addCharacter: PASS")
    else:
        print("duplicate addCharacter: FAIL")

    #Test setActive
    if not manager.setActive("Not in dict","Not in dict"):
        print("setActive: PASS")
    else:
        print("setActive: FAIL")

    if manager.getActive("discordName") == False:
        print("getActive: Pass")
    else:
        print("getActive: FAIL")

    if manager.setActive("playerName","discordName"):
        print("setActive: PASS")
    else:
        print("setActive: FAIL")

    if manager.getActive("discordName") == "playerName":
        print("getActive: Pass")
    else:
        print("getActive: FAIL")
     #Test setClass
    manager.setRace("discordName","Minotaur")
    manager.roll("discordName","str")
    
estebanTests()
