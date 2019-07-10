
class Monster:
    def __init__(self, name):
        self.name = name
        self.meta = ""
        self.armorClass = ""
        self.hp = ""
        self.speed = ""
        self.stre = ""
        self.dex = ""
        self.con = ""
        self.inte = ""
        self.wis = ""
        self.cha = ""
        self.savingThrows = ""
        self.skills = ""
        self.languages = ""
        self.challenge = ""
        self.damageImmunities = ""
        self.senses = []
        self.traits = []
        self.actions = []
        self.legendaryActions = ""
        self.img = ""

    def __str__(self):
        output = ""
        output += "Name" + ": " + str(self.name) + "\n"
        output += "meta" + ": " + str(self.meta) + "\n"
        output += "Armor Class" + ": " + str(self.armorClass) + "\n"
        output += "hp" + ": " + str(self.hp) + "\n"
        output += "speed" + ": " + str(self.speed) + "\n"
        output += "str" + ": " + str(self.stre) + "\n"
        output += "dex" + ": " + str(self.dex) + "\n"
        output += "con" + ": " + str(self.con) + "\n"
        output += "int" + ": " + str(self.inte) + "\n"
        output += "wis" + ": " + str(self.wis) + "\n"
        output += "cha" + ": " + str(self.cha) + "\n"
        output += "savingThrows" + ": " + str(self.savingThrows) + "\n"
        if len(self.skills) > 0:
            output += "skills" + ": " + str(self.skills) + "\n"
        output += "languages" + ": " + str(self.languages) + "\n"
        output += "challenge" + ": " + str(self.challenge) + "\n"
        output += "damageImmunities" + ": " + str(self.damageImmunities) + "\n"
        if len(self.senses) > 0:
            output += "senses" + ": " + "\n"
            for sense in self.senses:
                output += "    " + sense + "\n"
        if len(self.traits) > 0:
            output += "traits" + ": " + "\n"
            for trait in self.traits:
                output += "    " + trait + "\n"
        if len(self.actions) > 0:
            output += "actions" + ": " + "\n"
            for action in self.actions:
                output += "    " + action + "\n"
        if len(str(self.legendaryActions)) > 0:
            output += "legendaryActions" + ": " + "\n"
            for legendaryAction in self.legendaryActions:
                output += "    " + legendaryAction + "\n"
        output += "img" + ": " + str(self.img) + "\n\n"
        return output

