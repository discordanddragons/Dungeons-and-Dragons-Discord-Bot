import json
from monster import Monster

class MonsterManager:
    def __init__(self):
        # load json and add a class for each class
        self.monsters = {}
        with open('./json/monsters.json', encoding="utf8") as f:
            data = json.load(f)
        for monster in data:
            self.monsters[monster["name"]] = Monster(monster["name"])
            self.monsters[monster["name"]].meta = monster["meta"]
            self.monsters[monster["name"]].armorClass = monster["Armor Class"]
            self.monsters[monster["name"]].hp = monster["Hit Points"].split()[0]
            self.monsters[monster["name"]].speed = monster["Speed"].split()[0]
            self.monsters[monster["name"]].stre = monster["STR"]
            self.monsters[monster["name"]].dex = monster["DEX"]
            self.monsters[monster["name"]].con = monster["CON"]
            self.monsters[monster["name"]].inte = monster["INT"]
            self.monsters[monster["name"]].wis = monster["WIS"]
            self.monsters[monster["name"]].cha = monster["CHA"]
            if "Saving Throws" in monster:
                self.monsters[monster["name"]].savingThrows = monster["Saving Throws"]
            if "Skills" in monster:
                self.monsters[monster["name"]].skills = monster["Skills"]
            if "Damage Immunities" in monster:
                self.monsters[monster["name"]].damageImmunities = monster["Damage Immunities"]
            if "Senses" in monster:
                self.monsters[monster["name"]].senses = monster["Senses"].split(",")
            self.monsters[monster["name"]].languages = monster["Languages"]
            self.monsters[monster["name"]].challenge = monster["Challenge"]
            if "Traits" in monster:
                traits = monster["Traits"].replace(".</strong></em>", ":").replace("</p>", "").replace("</strong></em>", "")
                self.monsters[monster["name"]].traits = traits.split("<p><em><strong>")
                self.monsters[monster["name"]].traits.pop(0)
            if "Actions" in monster:
                actions = monster["Actions"].replace("</p>", "").replace(".</strong></em>", ":")
                self.monsters[monster["name"]].actions = actions.split("<p><em><strong>")
                self.monsters[monster["name"]].actions.pop(0)
            if "Legendary Actions" in monster:
                lactions = monster["Legendary Actions"].replace("</p>", "").replace(".</strong></em>", ":").replace("</strong></em>", "")
                self.monsters[monster["name"]].legendaryActions = lactions.split("<p><em><strong>")
                self.monsters[monster["name"]].legendaryActions.pop(0)
            self.monsters[monster["name"]].img = monster["img_url"]

    def __str__(self):
        output = ""
        for monster in self.monsters:
            output += monster + ": " + str(self.monsters[monster].name) + "\n"
            output += "meta" + ": " + str(self.monsters[monster].meta) + "\n"
            output += "Armor Class" + ": " + str(self.monsters[monster].armorClass) + "\n"
            output += "hp" + ": " + str(self.monsters[monster].hp) + "\n"
            output += "speed" + ": " + str(self.monsters[monster].speed) + "\n"
            output += "str" + ": " + str(self.monsters[monster].stre) + "\n"
            output += "dex" + ": " + str(self.monsters[monster].dex) + "\n"
            output += "con" + ": " + str(self.monsters[monster].con) + "\n"
            output += "int" + ": " + str(self.monsters[monster].inte) + "\n"
            output += "wis" + ": " + str(self.monsters[monster].wis) + "\n"
            output += "cha" + ": " + str(self.monsters[monster].cha) + "\n"
            output += "savingThrows" + ": " + str(self.monsters[monster].savingThrows) + "\n"
            if len(self.monsters[monster].skills) > 0:
                output += "skills" + ": " + str(self.monsters[monster].skills) + "\n"
            output += "languages" + ": " + str(self.monsters[monster].languages) + "\n"
            output += "challenge" + ": " + str(self.monsters[monster].challenge) + "\n"
            output += "damageImmunities" + ": " + str(self.monsters[monster].damageImmunities) + "\n"
            if len(self.monsters[monster].senses) > 0:
                output += "senses" + ": " + "\n"
                for sense in self.monsters[monster].senses:
                    output += "    " + sense + "\n"
            if len(self.monsters[monster].traits) > 0:
                output += "traits" + ": " + "\n"
                for trait in self.monsters[monster].traits:
                    output += "    " + trait + "\n"
            if len(self.monsters[monster].actions) > 0:
                output += "actions" + ": " + "\n"
                for action in self.monsters[monster].actions:
                    output += "    " + action + "\n"
            if len(str(self.monsters[monster].legendaryActions)) > 0:
                output += "legendaryActions" + ": " + "\n"
                for legendaryAction in self.monsters[monster].legendaryActions:
                    output += "    " + legendaryAction + "\n"
            output += "img" + ": " + str(self.monsters[monster].img) + "\n\n"
        return output

