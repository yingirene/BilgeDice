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

    def keep(self, dice, game):
        ai_keep_list = []
        if self.pid == 1:
            #Monty: Aiming for Qualifiers then Highest Score
            dice_copy = [d for d in dice]
            count_unqual = 0
            if not self.isQualified():
                for q_ind in range(len(self.qualified)):
                    if not self.qualified[q_ind]:
                        curr_qual = game.qualifiers[q_ind]
                        if curr_qual in dice_copy:
                            dice_copy.remove(curr_qual)
                            ai_keep_list.append(curr_qual)
                            self.setQualified(q_ind)
                        else:
                            count_unqual += 1
            #Choose values > 6; leave <= 3 if not qualified
            sorted_dice = sorted(dice_copy, reverse=True) 
            if not self.isQualified():
                #Leave <= count_unqual + 1
                if len(sorted_dice) <= (count_unqual + 1):
                    if len(ai_keep_list) <= 0:
                        #Keep at least 1 value
                        ai_keep_list = sorted_dice[0]
                else:
                    ai_keep_list.extend(sorted_dice[:-(count_unqual + 1)])
            else:
                ai_keep_list.extend([sd for sd in sorted_dice if sd > 4])

        elif self.pid == 2:
            #Krawk: Aiming for Highest Score ignoring Qualifiers
            ai_keep_list.extend([d for d in dice if d > 4])
            
        elif self.pid == 3:
            #Bill: Random Brute Force Choice
            num_to_keep = random.randint(1,len(dice))
            rand_ind = random.sample(range(0,len(dice)), num_to_keep)
            for d_ind in rand_ind:
                ai_keep_list.append(dice[d_ind])

        else:
            print "ERROR: invalid pid"
            exit(1)
        if len(ai_keep_list) < 1:
                ai_keep_list.append(max(dice))
        Player.keep(self, ai_keep_list)


players = {"You": Player("You", 0), "Monty": AI("Monty", 1), "Krawk": AI("Krawk", 2), "Bill": AI("Bill", 3)}


class Game:
    def __init__(self):
        self.qualifiers = [random.randint(1,6), random.randint(1,6)]
        self.numTurn = 0
        self.num_active_players = NUM_PLAYERS

    def startGame(self):
        self.qualifiers = [random.randint(1,6), random.randint(1,6)]
        self.numTurn = 0
        self.num_active_players = NUM_PLAYERS
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
                keepList = [int(k) for k in keepList]
                if len(keepList) == 1:
                    print keepList
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
                        #Account for number of explicit values
                        dice_copy.remove(int(keep_val))
                if not is_valid_keep:
                    continue
                player.keep(keepList)
                break
        else:
            keepList = player.keep(dice_vals, self)

        #Check if player is qualified after the move
        if not player.isQualified():
            for q_ind in range(len(self.qualifiers)):
                if keepList and self.qualifiers[q_ind] in keepList:
                    player.setQualified(q_ind)

        #Check if player is still active
        if not player.canMove():
            self.num_active_players -= 1
            print player.name + " is done."

    def printTurn(self):
        print "-- TURN " + str(self.numTurn) + " --"
        print "Current Hands:"
        for name in PLAYER_NAMES:
            handMsg = " have " if (name == "You") else " has "
            print name + handMsg + "the hand: " + " ".join(str(hand_val) for hand_val in players[name].hand)
        print "The qualifiers are " + " and ".join(str(q_val) for q_val in self.qualifiers)

    def getQualified(self):
        ret = []
        for (k,v) in players.items():
            if v.isQualified():
                ret.append(v)
        return ret

    def printQualified(self, qual_list):
        for p in qual_list:
            name = p.name
            qualMsg = " are " if (name == "You") else " is "
            print name + qualMsg + "qualified."

    def isOver(self):
        if self.num_active_players <= 0:
            return True
        return False

    def printScores(self):
        qual_players = self.getQualified()
        scoreMsg = "final" if self.isOver() else "current"
        print "The " + scoreMsg + " scores are: "
        max_total = 0
        winner_name = ""
        for k,v in players.items():
            total = sum(v.hand)
            total_msg = " have " if YOUR_NAME == "You" else " has "
            print k + total_msg + "a total of " + str(total)
            if v in qual_players:
                if total > max_total:
                    max_total = total
                    winner_name = k
            else:
                print "But isn't qualified."
        if self.isOver():
            win_msg = " are " if winner_name == "You" else " is "
            print winner_name + win_msg + "the winner!!!"

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
            for (k,v) in players.items():
                currPlayer = v
                if currPlayer.canMove():
                    self.makeMove(currPlayer)
            self.numTurn += 1

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
