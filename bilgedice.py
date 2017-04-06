'''
A text-only console version of the game Bilge Dice from Neopets
'''
import sys
import random

PLAYER_NAMES = ["Monty", "Krawk", "Bill"]
NUM_PLAYERS = 4
NUM_DICE = 6

class Player:
    def __init__(self, name, pid):
        self.name = name
        self.pid = pid
        self.qualified  = [False, False]
        self.hand = []

    def keep(self, list):
        self.hand.extend(list)
        if len(self.hand) == NUM_DICE:
            self.canMove = False
        return list

    def canMove(self):
        return len(self.hand) < NUM_DICE

    def setQualified(self, index):
        self.qualified[index] = True

    def isQualified(self):
        return not False in self.qualified

    def reset(self):
        self.qualified = [False, False]
        self.hand = []

class AI(Player):
    def __init__(self, name, pid):
        Player.__init__(self, name, pid)

    def keep(self, dice):
        ai_keep_list = []
        if self.pid == 1:
            print "Monty"
        elif self.pid == 2:
            print "Krawk"
        elif self.pid == 3:
            print "Bill"
        else:
            print "ERROR: invalid pid"
            exit(1)
        Player.keep(self, ai_keep_list)


players = {"You": Player("You", 0), "Monty": AI("Monty", 1), "Krawk": AI("Krawk", 2), "Bill": AI("Bill", 3)}


class Game:
    def __init__(self):
        self.qualifiers = [random.randint(1,6), random.randint(1,6)]
        self.numTurn = 0

    def startGame(self):
        self.numTurn = 0
        for (k,v) in players.items():
            v.reset()

    def makeMove(self, player):
        #Print out new dice values
        num_rem_dice = NUM_DICE - len(player.hand)
        dice_vals = random.sample(range(1,7), num_rem_dice)
        

        keepList = []
        if player.name == YOUR_NAME:
            print "Keep at least one of the following: "
            print str(dice_vals)
            while True:
                playerIn = raw_input("Which values will you keep? (Separate with spaces): ")
                keepList = str(playerIn).split()
                if len(keepList) < 1:
                    print "You must keep at least one value!"
                    continue
                dice_copy = [x for x in dice_vals]
                is_valid_keep = True
                for keep_val in keepList:
                    if int(keep_val) not in dice_copy:
                        print "ERROR: invalid values! Please choose again."
                        is_valid_keep = False
                        break
                    else:
                        dice_copy.remove(int(keep_val))
                if not is_valid_keep:
                    continue
                player.keep(keepList)
                break
        else:
            keepList = player.keep(dice_vals)

        #Check if player is qualified after the move
        if not player.isQualified():
            for q_ind in range(len(self.qualifiers)):
                if keepList and self.qualifiers[q_ind] in keepList:
                    player.setQualified(q_ind)
        self.numTurn = (self.numTurn + 1) % NUM_PLAYERS

    def printTurn(self):
        print "Current Hands:"
        for name in PLAYER_NAMES:
            handMsg = " have " if (name == "You") else " has "
            print name + handMsg + "the hand: " + " ".join(str(hand_val) for hand_val in players[name].hand)
        print "The qualifiers are " + " and ".join(str(q_val) for q_val in self.qualifiers)

    def printQualified(self):
        for name in PLAYER_NAMES:
            if players[name].isQualified():
                qualMsg = " are " if (name == "You") else " is "
                print name + qualMsg + "qualified."

    def isOver(self):
        if self.numTurn == NUM_DICE:
            return True
        return False

    def printScores(self):
        scoreMsg = "final" if self.isOver() else "current"
        print "The " + scoreMsg + " scores are: "
        max_total = 0
        winner_name = ""
        for k,v in players.items():
            total = str(sum(v.hand))
            print k + " has a total of " + total
            if total > max_total:
                max_total = total
                winner_name = k
        if self.isOver():
            print winner_name + " is the winner!!!"

    def runGame(self):
        while True:
            if self.isOver():
                self.printScores()
                playerIn = raw_input("Would you like to continue playing?: ")
                if playerIn == "Yes":
                  self.startGame()  
                else:
                    print "Quitting Game."
                    break
            self.printTurn()
            self.printQualified()
            for (k,v) in players.items():
                currPlayer = v
                if currPlayer.canMove:
                    self.makeMove(currPlayer)

isMultiplayer = False
#isMultiplayer = (raw_input("Would you like to play multiplayer?: ") == "Yes") ? True : False

#Handle multiplayer settings
if isMultiplayer:
    if "You" in player:
        YOUR_NAME = raw_input("Enter your nickname: ")
        players[YOUR_NAME] = player["You"]
        players[YOUR_NAME].name = YOUR_NAME
        players.pop("You", None)
else:
    YOUR_NAME = "You"

PLAYER_NAMES.append(YOUR_NAME)

Game().runGame();
