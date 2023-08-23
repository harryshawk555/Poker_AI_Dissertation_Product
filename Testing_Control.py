import pandas as pd
from handCheck import Check
from initialize import Initialize
from aiPrep import *
from ShowdownCalc import *
from randomAgent import *
from gtoAgent import *
from equityAgent import *
import random

global button

global outcomeList

button = False
Deck = Initialize()

def GameTestEnvironment():
    global button
    global aStack
    global bStack
    global outcomeList
    AllIn = False

    agent = random.randint(1,3)

    aStack = 250
    bStack = 250

    actionTaken = False
    board = []
    aHandEnum = []
    bHandEnum = []
    pot = 0
    actions = 0

    if button == True:
        aCurrBet = 1
        bCurrBet = 2

    else:
        aCurrBet = 2
        bCurrBet = 1
    aStack -= aCurrBet
    bStack -= bCurrBet
    handHist = []
    betDiff = 0
    board = random.sample(Deck, 12)
    Rboard = []
    aHand = [board[0], board[2]]
    bHand = [board[1], board[3]]
    board.pop(0)
    board.pop(0)
    board.pop(0)
    board.pop(0)

    action = button
    pbet = ''
    bet = ''
    action_finished = False
    hand_finished = False
    AllIn = False


    while hand_finished != True:
        actionTaken = False
        if len(Rboard) > 0:
            aCurrBet = 0
            bCurrBet = 0
        pbet = ''
        bet = ''
        betSize = bCurrBet
        pBetSize = aCurrBet
        if bStack == 0 and aStack == 0:
            action_finished = True
        while action_finished != True and AllIn != True:
            handHist.append([[aCurrBet,pbet],[bCurrBet,bet], [aStack,bStack]])
            betVal = max([aCurrBet,bCurrBet])
            if action == True and aStack>0:
                prevABet = pBetSize
                pbet, pBetSize = randomAgent(Rboard,pot,betVal)
                if pBetSize > aStack:
                    pBetSize = aStack
                    pbet = 'AllIn'
                if pBetSize > bStack:
                    pBetSize = bStack
                    pbet = 'AllIn'
                if pBetSize < 0:
                    pBetSize = 0
                if pBetSize> 0:
                    aCurrBet = pBetSize
                    aStack -= aCurrBet - prevABet

            elif bStack > 0:
                prevBBet = betSize
                if agent == 1:
                    bet,betSize = randomAgent(Rboard,pot,betVal)
                if agent == 2:
                    bet,betSize = equityAgent(Rboard,pot,betVal,bHand,button,actionTaken,AllIn,(bStack+prevBBet))
                if agent == 3:
                    bet,betSize = gtoAgent(Rboard,pot,betVal,bHand,button,actionTaken,AllIn,(bStack+prevBBet))

                if type(bet) is tuple:
                    betSize = bet[1]
                    bet = bet[0]
                if betSize > aStack:
                    betSize = aStack
                    bet = 'AllIn'
                if betSize > bStack:
                    betSize = bStack
                    bet = 'AllIn'
                if betSize < 0:
                    betSize = 0
                if betSize > 0:
                    bCurrBet = betSize
                    bStack -= bCurrBet - prevBBet
            action = not(action)
            if pbet == 'AllIn' and bet == 'AllIn':
                action_finished = True
                AllIn = True


            handHist.append([[aCurrBet,pbet],[bCurrBet,bet], [aStack,bStack]])
            if handHist[actions][0][1] == 'AllIn' and (handHist[actions][1][1] == 'Call' or handHist[actions][1][1] == 'AllIn'):
                aCurrBet = max([aStack,bStack])
                bCurrBet = max([aStack,bStack])
                pbet = 'AllIn'
                bet = 'AllIn'
                aStack = 0
                bStack = 0
            
            if handHist[actions][1][1] == 'AllIn' and (handHist[actions][0][1] == 'Call' or handHist[actions][0][1] == 'AllIn'):
                aCurrBet = max([aStack,bStack])
                bCurrBet = max([aStack,bStack])
                pbet = 'AllIn'
                bet = 'AllIn'
                aStack = 0
                bStack = 0
            
            if handHist[actions][0][1] == 'Check' and handHist[actions][1][1] == 'Call':
                bet = 'Check'
                action_finished = True

            if handHist[actions][1][1] == 'Check' and handHist[actions][0][1] == 'Call':
                pbet = 'Check'
                action_finished = True

            if handHist[actions][0][1] == 'AllIn' and handHist[actions][1][1] == 'Check':
                bet = 'Fold'
                action_finished = True

            if handHist[actions][1][1] == 'AllIn' and handHist[actions][0][1] == 'Check':
                pbet = 'Fold'
                action_finished = True

            if handHist[actions][0][1] == 'AllIn' and handHist[actions][1][1] == 'Raise':
                bet = 'AllIn'
                action_finished = True

            if handHist[actions][1][1] == 'AllIn' and handHist[actions][0][1] == 'Raise':
                pbet = 'AllIn'
                action_finished = True

            if len(Rboard) == 0:
                if pbet =='Call' or bet == 'Call' or bet == 'Check' or pbet == 'Check':
                    action_finished = True
                    pot += betSize*2
                elif pbet =='Fold' or bet == 'Fold':
                    action_finished = True
                    hand_finished = True
                    if pbet == 'Fold':
                        bStack += pot
                        if pot > round(0.75*250):
                            outcome = 0
                        else:
                            outcome = 1
                    else:
                        aStack += pot
                        if pot > round(0.75*250):
                            outcome = 2
                        else:
                            outcome = 3

            else:
                if button == True and pbet == 'Check':
                    action_finished = True
                elif button == False and bet == 'Check': 
                    action_finished = True
                elif pbet == 'Call' or bet == 'Call':
                    action_finished = True
                elif pbet =='Fold' or bet == 'Fold':
                    action_finished = True
                    hand_finished = True
                    if pbet == 'Fold':
                        bStack += pot
                        if pot > round(0.75*aStack):
                            outcome = 0
                        else:
                            outcome = 1
                    else:
                        aStack += pot
                        if pot > round(0.75*aStack):
                            outcome = 3
                        else:
                            outcome = 2
            if betSize > bStack:
                betSize = bStack
                bet = 'AllIn'
            if betSize > aStack:
                betSize = aStack
                bet = 'AllIn'
            if pBetSize > aStack:
                pBetSize = aStack
                pbet = 'AllIn'
            if pBetSize > bStack:
                pBetSize = bStack
                pbet = 'AllIn'
            if aCurrBet > aStack:
                aCurrBet = aStack
            if bCurrBet > bStack:
                bCurrBet = bStack
            if aStack < 0:
                aCurrBet = 0
            if bStack < 0:
                bCurrBet = 0
            if aStack <= 0 and bStack <=0:
                action_finished = True
            if actionTaken == False:
                actionTaken = True


            actions += 1

        if hand_finished == False:
            if len(Rboard) == 0:
                board.pop(0)          
                Rboard.append(board[0])
                Rboard.append(board[1])
                Rboard.append(board[2])
                board.pop(0)
                board.pop(0)
                board.pop(0)
                handHist.append([[aCurrBet,pbet],[bCurrBet,bet]])
                              
            elif len(Rboard) == 3:
                board.pop(0)          
                Rboard.append(board[0])
                board.pop(0)
                handHist.append([[aCurrBet,pbet],[bCurrBet,bet]])
            elif len(Rboard) == 4:
                board.pop(0)          
                Rboard.append(board[0])
                board.pop(0)
                handHist.append([[aCurrBet,pbet],[bCurrBet,bet]])
            elif len(Rboard) == 5:
                hand_finished = True
                action_finished = True
                aHandEnum = HandCheck([Rboard,aHand])
                bHandEnum = HandCheck([Rboard,bHand])
                winner = ShowdownHands(aHandEnum,bHandEnum)
                handHist.append([[aCurrBet,pbet],[bCurrBet,bet]])
                if winner == 'a':
                    aStack += pot
                    if pot > round(0.75*aStack):
                        outcome = 2
                    else:
                        outcome = 3
                elif winner == 'b':
                    bStack += pot
                    if pot > round(0.75*aStack):
                        outcome = 0
                    else:
                        outcome = 1
                elif winner == 'chop':
                    outcome = 0
                    aStack += 0.5*pot
                    bStack += 0.5*pot
        action_finished = False
        pot += aCurrBet + bCurrBet
    print(actions)  
    outcomeList.append(outcome)
       

outcomeList = []
for i in range(0,8000):
    GameTestEnvironment()
    prc = i/8000
    print('%s' %(prc))

Test_Outcomes = pd.DataFrame(outcomeList)
Test_Outcomes.to_csv('controlTestOutcomes.csv')