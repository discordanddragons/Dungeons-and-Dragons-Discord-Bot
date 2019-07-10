
class Game:
    def __init__(self, name, size, active):
        self.name = name
        self.active = active
        self.size = size
        self.description = ""
        self.players = {}
        self.encounters = {}

    def __str__(self):
        output = ""
        output += "Name: " + self.name + "\n"
        output += "Active: " + str(self.active) + "\n"
        output += "Max Players: " + str(self.size) + "\n"
        for player in self.players:
            output += player + ": " + str(self.players[player]) + "\n"
        for encounter in self.encounters:
            output += encounter+": "+str(self.encounters[encounter])+"\n"
        return output
