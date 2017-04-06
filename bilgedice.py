# -*- coding: utf-8 -*-
'''
A text-only console version of the game Bilge Dice from Neopets
'''
import sys
import random

PLAYER_NAMES = ["Monty", "Grimtooth", "Deadeye"]
NUM_PLAYERS = 4
NUM_DICE = 6

class Player:
    def __init__(self, name, pid):
        self.name = name
        self.pid = pid
        self.qualified  = [False, False]
        self.qualifiers = []
        self.hand = []

    def keep(self, list):
        self.hand.extend(list)
        return list

    def canMove(self):
        return (len(self.hand) + len(self.qualifiers)) < NUM_DICE

    def setQualified(self, index):
        self.qualified[index] = True

    def isQualified(self):
        return not False in self.qualified

    def reset(self):
        self.qualified = [False, False]
        self.qualifiers = []
        self.hand = []

class AI(Player):
    def __init__(self, name, pid):
        Player.__init__(self, name, pid)

    def keep(self, dice, game):
        ai_keep_list = []
        num_chosen = 0
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
                            #ai_keep_list.append(curr_qual)
                            self.qualifiers.append(curr_qual)
                            num_chosen += 1
                            self.setQualified(q_ind)
                        else:
                            count_unqual += 1
            #Choose values > 6; leave <= 3 if not qualified
            sorted_dice = sorted(dice_copy, reverse=True) 
            if not self.isQualified() and len(sorted_dice) > 0:
                #Leave <= count_unqual + 1
                if len(sorted_dice) <= (count_unqual + 1):
                    if len(ai_keep_list) <= 0:
                        #Keep at least 1 value
                        ai_keep_list = sorted_dice[0]
                else:
                    ai_keep_list.extend(sorted_dice[:-(count_unqual + 1)])
            else:
                ai_keep_list.extend([sd for sd in sorted_dice if sd > 5])

        elif self.pid == 2:
            dice_copy = [d for d in dice]  
            count_unqual = 0
            #Grimtooth: Aiming for Highest Score and Qualifiers as low-priority
            if not self.isQualified():
                if sum(self.hand) > game.max_score:
                    for q_ind in range(len(self.qualified)):
                        if not self.qualified[q_ind]:
                            curr_qual = game.qualifiers[q_ind]
                            if curr_qual in dice_copy:
                                dice_copy.remove(curr_qual)
                                #ai_keep_list.append(curr_qual)
                                self.qualifiers.append(curr_qual)
                                num_chosen += 1
                                self.setQualified(q_ind)
                            else:
                                count_unqual += 1
            ai_keep_list.extend([d for d in dice if d > 5][:-(count_unqual)])
            
        elif self.pid == 3:
            #Deadeye: Random Brute Force Choice
            num_to_keep = random.randint(1,len(dice))
            rand_ind = random.sample(range(0,len(dice)), num_to_keep)
            for d_ind in rand_ind:
                if dice[d_ind] in game.qualifiers:
                    for gq_ind in range(len(game.qualifiers)):
                        if game.qualifiers[gq_ind] == dice[d_ind] and not self.qualified[gq_ind]:
                            self.qualified[gq_ind] = True
                            self.qualifiers.append(dice[d_ind])
                            num_chosen += 1
                            break
                else:
                    ai_keep_list.append(dice[d_ind])

        else:
            print "ERROR: invalid pid"
            exit(1)
        if not isinstance(ai_keep_list, list):
            ai_keep_list = [ai_keep_list]
        if num_chosen < 1 and len(ai_keep_list) < 1:
                ai_keep_list.append(max(dice))
        Player.keep(self, ai_keep_list)


players = {"You": Player("You", 0), "Monty": AI("Monty", 1), "Grimtooth": AI("Grimtooth", 2), "Deadeye": AI("Deadeye", 3)}


class Game:
    def __init__(self):
        self.qualifiers = [random.randint(1,6), random.randint(1,6)]
        self.numTurn = 0
        self.num_active_players = NUM_PLAYERS
        self.max_score = 0
        self.winner_name = []
        self.num_games = 0
        self.num_wins = 0
        self.prev_is_win = False
        self.best_win_streak = 0
        self.curr_win_streak = 0

    def startGame(self):
        self.qualifiers = [random.randint(1,6), random.randint(1,6)]
        self.numTurn = 0
        self.num_active_players = NUM_PLAYERS
        self.max_score = 0
        self.winner_name = []
        for (k,v) in players.items():
            v.reset()

    def makeMove(self, player):
        #Print out new dice values
        num_rem_dice = NUM_DICE - len(player.hand) - len(player.qualifiers)
        dice_vals = [random.randint(1,6) for _ in [0] * num_rem_dice]

        keepList = []
        if player.name == YOUR_NAME:
            while True:
                print "Your Rolls:"
                print str(dice_vals)
                playerIn = raw_input("Select at least one die value: ").rstrip().lstrip()
                if playerIn.lower() == "quit":
                    print "Quitting game."
                    exit(1)
                elif playerIn.lower() == "help":
                    self.printHelp()
                    continue
                elif playerIn.lower() == "score":
                    self.printScores()
                    continue
                elif playerIn.lower() == "stats":
                    self.printStats()
                    continue
                keepList = str(playerIn).split()
                if not isinstance(keepList, list):
                    keepList = [int(keepList)]
                isInvalid = False
                for k_ind in range(len(keepList)):
                    if not keepList[k_ind].isdigit():
                        print "ERROR: please enter a number or a valid command."
                        isInvalid = True
                        break
                if isInvalid:
                    continue
                keepList = [int(k) for k in keepList]
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
                #Separate the qualifiers from the rest of the hand
                keepList_copy = [kp for kp in keepList]
                for k_val in keepList_copy:
                    for sq_ind in range(len(self.qualifiers)):
                        if self.qualifiers[sq_ind] == k_val and not player.qualified[sq_ind]:
                            player.qualified[sq_ind] = True
                            player.qualifiers.append(k_val)
                            keepList.remove(k_val)
                            break
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

    def printTurn(self):
        print "-- TURN " + str(self.numTurn) + " --"
        print "Current Hands:"
        sep_msg = " " if self.numTurn == 0 else " | "
        for name in PLAYER_NAMES:
            handMsg = " have " if (name == "You") else " has "
            print name + handMsg + "the hand: " + " ".join(str(hand_val) for hand_val in players[name].hand) + sep_msg + '\033[1m' + " ".join(str(qual_val) for qual_val in players[name].qualifiers) + '\033[0m'
        print "The qualifiers are " + " and ".join(str(q_val) for q_val in self.qualifiers)
        print ""

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
        print ""
        qual_players = self.getQualified()
        scoreMsg = "\033[1m FINAL SCORES \033[0m" if self.isOver() else "Current Scores"
        print "-- " + scoreMsg + " --"
        for name in PLAYER_NAMES:
            k = name
            v = players[k]
            total = sum(v.hand)
            total_msg = "r" if v.name == "You" else "'s"
            print k + total_msg + " score: " + str(total) + " | Qualifies: " + str(v.isQualified())
            if v in qual_players:
                if total > self.max_score:
                    self.max_score = total
                    self.winner_name = [k]
                if total == self.max_score:
                    if not k in self.winner_name:
                        self.winner_name.append(k)
        if self.isOver():
            self.num_games += 1
            print ""
            if len(self.winner_name) < 1:
                print "Everyone loses!"
                return
            if len(self.winner_name) > 1:
                print "It's a tie!"
                join_msg = (", ".join(self.winner_name[:-1]) + ",") if len(self.winner_name) > 2 else self.winner_name[0]
                print "Between " + join_msg + " and " + self.winner_name[-1]
                if not YOUR_NAME in self.winner_name:
                    print "You lose!"
                return
            if self.winner_name[0] == YOUR_NAME:
                print "Congratulations!!"
                self.num_wins += 1
                if self.prev_is_win:
                    self.curr_win_streak += 1
                else:
                    if self.curr_win_streak > self.best_win_streak:
                        self.best_win_streak = self.curr_win_streak
                    self.curr_win_streak = 1
                self.prev_is_win = True
            else:
                self.prev_is_win = False
            win_msg = " are " if self.winner_name[0] == "You" else " is "
            print self.winner_name[0] + win_msg + "the winner!"
        print "--------------------\n"

    def printStats(self):
        print ""
        print "-- Current Stats --"
        print '{0: ^6}'.format("Games") + "|" + '{0: ^6}'.format("Wins") + "|" + '{0: ^16}'.format("Current Streak") + "|" + '{0: ^16}'.format("Best Streak")
        print "------|------|----------------|----------------"
        print '{0: ^6}'.format(self.num_games) + "|" + '{0: ^6}'.format(self.num_wins) + "|" + '{0: ^16}'.format(self.curr_win_streak) + "|" + '{0: ^16}'.format(self.best_win_streak)
        print ""

    def printHelp(self):
        print """
----------------------------------------------------------------------------------------------
Summary:
You are trying to get a higher total score than your opponents: Monty, Grimtooth, and Deadeye.

How to play:
At the start of the game, there are six dice.
On each turn, choose at least 1 value and those dice are removed from play.
You must select at least one die value to keep before you can re-roll.
You continue until all six dice are kept.

In order to qualify for a round, you need to obtain the qualifier values.
The qualifiers are not included in the total score.
The qualifying player with the highest total score wins.

Notes:
    Game looks best in a window of minimum width: 95 columns
    Available commands: score, stats, help, quit
----------------------------------------------------------------------------------------------
        """

    def printIntro(self):
        welcome_banner = """
                    _ _ _ ____ _    ____ ____ _  _ ____    ___ ____ 
                    | | | |___ |    |    |  | |\/| |___     |  |  | 
                    |_|_| |___ |___ |___ |__| |  | |___     |  |__| 
                                                            
        """
        title_banner = """
            ██████╗ ██╗██╗      ██████╗ ███████╗    ██████╗ ██╗ ██████╗███████╗
            ██╔══██╗██║██║     ██╔════╝ ██╔════╝    ██╔══██╗██║██╔════╝██╔════╝
            ██████╔╝██║██║     ██║  ███╗█████╗      ██║  ██║██║██║     █████╗  
            ██╔══██╗██║██║     ██║   ██║██╔══╝      ██║  ██║██║██║     ██╔══╝  
            ██████╔╝██║███████╗╚██████╔╝███████╗    ██████╔╝██║╚██████╗███████╗
            ╚═════╝ ╚═╝╚══════╝ ╚═════╝ ╚══════╝    ╚═════╝ ╚═╝ ╚═════╝╚══════╝
                                                                               

        """

        print welcome_banner
        print title_banner

    def runGame(self):
        self.printIntro()
        self.printHelp()
        while True:
            if self.isOver():
                self.printTurn()
                print ""
                self.printScores()
                while self.isOver():
                    playerIn = raw_input("Play again? (yes/no): ")
                    if playerIn.lower() == "yes":
                        self.startGame()  
                    elif playerIn.lower() == "help":
                        self.printHelp()
                    elif playerIn.lower() == "score":
                        self.printScores()
                    elif playerIn.lower() == "stats":
                        self.printStats()
                    elif "quit" or "no":
                        print "Quitting Game."
                        exit(1)
                    else:
                        print "ERROR: invalid command."
                print ""
            self.printTurn()
            for (k,v) in players.items():
                currPlayer = v
                if currPlayer.canMove():
                    self.makeMove(currPlayer)
            self.numTurn += 1
            print ""

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
