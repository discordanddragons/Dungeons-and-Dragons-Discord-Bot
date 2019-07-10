
class Encounter:
    def __init__(self, name, active):
        self.name = name
        self.active = active
        self.monsters = []
        self.description = ""
        self.initiativeTrack = []

    def __str__(self):
        output = ""
        output += "Name: " + self.name + "\n"
        output += "Active: " + str(self.active) + "\n"
        if len(self.monsters) > 0:
            output += "Monsters: \n"
            for elem in self.monsters:
                output += "    " + elem + "\n"
        return output

    # def startEncounter(self):
        # All players and monsters roll for initiative (1d20 + dex modifier)
        # Add players/monsters to initiativeTrack list to keep track of who is doing actions in what order
        # If there is a tie ???? re roll to see who goes first?? randomly pick???
        # Whoever is in the 0 position is the person taking their turn
        # If there are 2 players next to each other ie: pos 0 and 1, have the bot listen to commands from either player
        # The player that sends their command first does their action and then moves to the back of the list
        # IE: 0(player) 1(player) 2(Monster) 3(player) 4(Monster) 5(player)
        # IE: Currently it is player 0's turn, if player 1 sends their command then that action goes through
        # IE: and the new list looks like this
        # IE: 0(player) 2(Monster) 3(player) 4(Monster) 5(player) 1(player)
        # IE: But we still wait for player 0 to do their action before moving to the next thing in the list
