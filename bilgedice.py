'''
A text-only console version of the game Bilge Dice from Neopets
'''
import sys
import random

PLAYER_NAMES = ["Monty", "Krawk", "Bill"]
NUM_PLAYERS = 4;
NUM_DICE = 6;

class Game:
    def __init__(self):
        self.qualifiers = [random.randint(1,6), random.randint(1,6)]
        self.isGameOver = true
        self.numTurn = 0

    def startGame(self):
        self.isGameOver = false

    def makeMove(self):
        self.numTurn = (self.numTurn + 1) % NUM_PLAYERS

class Player:
    def __init__(self, pid):
        self.pid = pid
        self.dice = []
        self.qualified  = [false, false]
        self.__canMove = true

    def keep(self, list):
        self.dice.extend(list)
        if len(self.dice) == NUM_DICE:
            self.canMove = false

    def canMove(self):
        return self.__canMove;

class Enemy(Player):
    def __init__(self, pid, name):
        Player.__init__(self, pid)
        self.name = name
