import json
import re

class ClassManager:
    def __init__(self):
        # load json and add a class for each class
        self.classes = {}
        with open('./json/classes.json', encoding="utf8") as f:
            data = json.load(f)
        for elem in data:
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

    def getClass(self,className):
        self.classes
    def __str__(self):
        output = ""
        for elem in self.classes:
            output += elem + ": \n"
            output += str(self.classes[elem])
        return output

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
