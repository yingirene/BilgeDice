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

    def can_move(self):
        return (len(self.hand) + len(self.qualifiers)) < NUM_DICE

    def set_qualified(self, index):
        self.qualified[index] = True

    def is_qualified(self):
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
            if not self.is_qualified():
                for q_ind in range(len(self.qualified)):
                    if not self.qualified[q_ind]:
                        curr_qual = game.qualifiers[q_ind]
                        if curr_qual in dice_copy:
                            dice_copy.remove(curr_qual)
                            #ai_keep_list.append(curr_qual)
                            self.qualifiers.append(curr_qual)
                            num_chosen += 1
                            self.set_qualified(q_ind)
                        else:
                            count_unqual += 1
            #Choose values > 6; leave <= 3 if not qualified
            sorted_dice = sorted(dice_copy, reverse=True) 
            if not self.is_qualified() and len(sorted_dice) > 0:
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
            if not self.is_qualified():
                if sum(self.hand) > game.max_score:
                    for q_ind in range(len(self.qualified)):
                        if not self.qualified[q_ind]:
                            curr_qual = game.qualifiers[q_ind]
                            if curr_qual in dice_copy:
                                dice_copy.remove(curr_qual)
                                self.qualifiers.append(curr_qual)
                                num_chosen += 1
                                self.set_qualified(q_ind)
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
        self.num_turn = 0
        self.num_active_players = NUM_PLAYERS
        self.max_score = 0
        self.winner_name = []
        #Initialize values for stats
        self.num_games = 0
        self.num_wins = 0
        self.best_win_streak = 0
        self.curr_win_streak = 0

    def startGame(self):
        self.qualifiers = [random.randint(1,6), random.randint(1,6)]
        self.num_turn = 0
        self.num_active_players = NUM_PLAYERS
        self.max_score = 0
        self.winner_name = []
        for (k,v) in players.items():
            v.reset()

    def make_move(self, player):
        #Print out new dice values
        num_rem_dice = NUM_DICE - len(player.hand) - len(player.qualifiers)
        dice_vals = [random.randint(1,6) for _ in [0] * num_rem_dice]

        keep_list = []
        if player.name == YOUR_NAME:
            while True:
                print "Your Rolls:"
                print str(dice_vals) + "\n"
                player_in = raw_input("Select at least one die value: ").rstrip().lstrip()
                if player_in.lower() == "quit":
                    print "Quitting game."
                    exit(1)
                elif player_in.lower() == "help":
                    self.print_help()
                    continue
                elif player_in.lower() == "score":
                    self.print_scores()
                    continue
                elif player_in.lower() == "stats":
                    self.print_stats()
                    continue
                keep_list = str(player_in).split()
                if not isinstance(keep_list, list):
                    keep_list = [int(keep_list)]
                is_invalid = False
                for k_ind in range(len(keep_list)):
                    if not keep_list[k_ind].isdigit():
                        print "ERROR: please enter a number or a valid command.\n"
                        is_invalid = True
                        break
                if is_invalid:
                    continue
                keep_list = [int(k) for k in keep_list]
                if len(keep_list) < 1:
                    print "ERROR: you must keep at least one value!\n"
                    continue
                dice_copy = [x for x in dice_vals]
                is_valid_keep = True
                for keep_val in keep_list:
                    if int(keep_val) not in dice_copy:
                        print "ERROR: invalid values! Please choose again.\n"
                        is_valid_keep = False
                        break
                    else:
                        #Account for number of explicit values
                        dice_copy.remove(int(keep_val))
                if not is_valid_keep:
                    continue
                #Separate the qualifiers from the rest of the hand
                keep_list_copy = [kp for kp in keep_list]
                for k_val in keep_list_copy:
                    for sq_ind in range(len(self.qualifiers)):
                        if self.qualifiers[sq_ind] == k_val and not player.qualified[sq_ind]:
                            player.qualified[sq_ind] = True
                            player.qualifiers.append(k_val)
                            keep_list.remove(k_val)
                            break
                player.keep(keep_list)
                break
        else:
            keep_list = player.keep(dice_vals, self)

        #Check if player is qualified after the move
        if not player.is_qualified():
            for q_ind in range(len(self.qualifiers)):
                if keep_list and self.qualifiers[q_ind] in keep_list:
                    player.set_qualified(q_ind)

        #Check if player is still active
        if not player.can_move():
            self.num_active_players -= 1

    def print_turn(self):
        print "-- TURN " + str(self.num_turn) + " --"
        print "Current Hands:"
        sep_msg = " " if self.num_turn == 0 else " | "
        for name in PLAYER_NAMES:
            hand_msg = " have " if (name == "You") else " has "
            print name + hand_msg + "the hand: " + " ".join(str(hand_val) for hand_val in players[name].hand) + sep_msg + '\033[1m' + " ".join(str(qual_val) for qual_val in players[name].qualifiers) + '\033[0m'
        print "\nThe qualifiers are " + " and ".join(str(q_val) for q_val in self.qualifiers)
        print ""

    def get_qualified(self):
        ret = []
        for (k,v) in players.items():
            if v.is_qualified():
                ret.append(v)
        return ret

    def print_qualified(self, qual_list):
        for p in qual_list:
            name = p.name
            qual_msg = " are " if (name == "You") else " is "
            print name + qual_msg + "qualified."

    def is_over(self):
        if self.num_active_players <= 0:
            return True
        return False

    def print_scores(self):
        print ""
        qual_players = self.get_qualified()
        score_msg = "\033[1m FINAL SCORES \033[0m" if self.is_over() else "Current Scores"
        print "-- " + score_msg + " --"
        for name in PLAYER_NAMES:
            k = name
            v = players[k]
            total = sum(v.hand)
            total_msg = "r" if v.name == "You" else "'s"
            print k + total_msg + " score: " + str(total) + " | Qualifies: " + str(v.is_qualified())
            if v in qual_players:
                if total > self.max_score:
                    self.max_score = total
                    self.winner_name = [k]
                if total == self.max_score:
                    if not k in self.winner_name:
                        self.winner_name.append(k)
        if self.is_over():
            self.num_games += 1
            print ""
            if len(self.winner_name) < 1:
                print "Everyone loses!"
            elif len(self.winner_name) > 1:
                print "It's a tie!"
                join_msg = (", ".join(self.winner_name[:-1]) + ",") if len(self.winner_name) > 2 else self.winner_name[0]
                print "Between " + join_msg + " and " + self.winner_name[-1]
                if not YOUR_NAME in self.winner_name:
                    print "You lose!"
            else:
                if self.winner_name[0] == YOUR_NAME:
                    print "Congratulations!!"
                    self.num_wins += 1
                    self.curr_win_streak += 1
                    if self.curr_win_streak > self.best_win_streak:
                        self.best_win_streak = self.curr_win_streak
                else:
                    self.curr_win_streak = 0
                win_msg = " are " if self.winner_name[0] == "You" else " is "
                print self.winner_name[0] + win_msg + "the winner!"
        if not self.is_over():
            print "\nThe qualifiers are " + " and ".join(str(q_val) for q_val in self.qualifiers)
        print "--------------------\n"

    def print_stats(self):
        print ""
        print "-- Current Stats --"
        print '{0: ^6}'.format("Games") + "|" + '{0: ^6}'.format("Wins") + "|" + '{0: ^16}'.format("Current Streak") + "|" + '{0: ^16}'.format("Best Streak")
        print "------|------|----------------|----------------"
        print '{0: ^6}'.format(self.num_games) + "|" + '{0: ^6}'.format(self.num_wins) + "|" + '{0: ^16}'.format(self.curr_win_streak) + "|" + '{0: ^16}'.format(self.best_win_streak)
        print "-------------------\n"

    def print_help(self):
        print """
-------------------------------------------------------------------------------------------
How to play:
At the start of the game, there are six dice.
On each turn, choose at least 1 value and those dice are removed from play.
You must select at least one die value to keep before you can re-roll.
You continue until all six dice are kept.

In order to qualify for a round, you need to obtain the qualifier values.
The qualifiers are not included in the total score.
The qualifying player with the highest total score wins.

Notes:
    Game looks best in a window of minimum width: 91 columns
    Available commands: score, stats, help, quit
-------------------------------------------------------------------------------------------
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

    def run_game(self):
        self.printIntro()
        self.print_help()
        while True:
            if self.is_over():
                self.print_turn()
                print ""
                self.print_scores()
                while self.is_over():
                    player_in = raw_input("Play again? (yes/no): ")
                    if player_in.lower() == "yes":
                        self.startGame()  
                    elif player_in.lower() == "help":
                        self.print_help()
                    elif player_in.lower() == "score":
                        self.print_scores()
                    elif player_in.lower() == "stats":
                        self.print_stats()
                    elif player_in.lower() ==  "quit" or player_in.lower() == "no":
                        print "Quitting Game."
                        exit(1)
                    else:
                        print "ERROR: invalid command.\n"
                print ""
            self.print_turn()
            for (k,v) in players.items():
                currPlayer = v
                if currPlayer.can_move():
                    self.make_move(currPlayer)
            self.num_turn += 1
            print ""

is_multiplayer = False
#is_multiplayer = (raw_input("Would you like to play multiplayer?: ") == "Yes") ? True : False

#Handle multiplayer settings
if is_multiplayer:
    if "You" in player:
        YOUR_NAME = raw_input("Enter your nickname: ")
        players[YOUR_NAME] = player["You"]
        players[YOUR_NAME].name = YOUR_NAME
        players.pop("You", None)
else:
    YOUR_NAME = "You"

PLAYER_NAMES.append(YOUR_NAME)

Game().run_game();
