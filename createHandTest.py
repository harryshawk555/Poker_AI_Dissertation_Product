from handCheck import Check
from createHandInit import Initialize
import random
from enum import Enum
import sys , json

board = []
wholeCards = []
hand = []
bestHand = []
count = 0
board = Initialize()
wholeCards = [board[0], board[1]]

board.pop(0)
board.pop(0)
for card in board:
    print(card.name)
print()
for card in wholeCards:
    print(card.name)
print()
hand = Check(board, wholeCards)
fullHandEnum = hand[0]
print(fullHandEnum.value, "\n")
bestHand = hand[1]
    
for card in bestHand:
    print(card.name)

print()