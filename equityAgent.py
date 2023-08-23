from MultiCheck import HandCheck,Hand
from gtoAgent import *
import random

def postFlopResponseEquity(hand,board,pot,betVal):
    equityReq = round((betVal/(pot+betVal))*100)
    fullHand = []
    valList = []
    for i in board:
        fullHand.append(i)
        valList.append(i.value+i.modif)
    for i in hand:
        fullHand.append(i)
        valList.append(i.value+i.modif)
    
    handArr = HandCheck([fullHand,hand])
    madeHand = False
    for i in handArr[4]:
        if i == True and madeHand == False:
            madeHand = True
        else:
            madeHand = False

    flush = handArr[4][0]
    straight = handArr[4][1]
    overs = handArr[4][2]

    if flush:
        if straight:
            if overs:
                outs = 21
            else:
                outs = 15
        else:
            outs = 9
    elif straight:
        if overs:
            outs = 14
        else:
            outs = 8
    elif overs:
        outs = 6
    else:
        outs = 0
    
    if outs > 0:
        if len(board) == 3:
            ctw = outs*4
        elif len(board) == 4:
            ctw = outs*2
        else:
            ctw = 0
    else:
        ctw = 0

        

    if madeHand == True:
        if handArr[0].value >=2 and handArr[3] >= 35+max(valList):
            betCall = random.randint(1,12)
            if betCall > 9:
                bet = round(0.4*(pot+betVal)) + 2*betVal
            elif betCall < 3:
                bet = 0
            else:
                bet = betVal
        
        elif handArr[0].value>=3:
            betCheck = random.randint(1,10)
            if betCheck > 8:
                bet = 0
            elif betCheck <3:
                bet = betVal
            else:
                bet = round(0.4*(pot+betVal)) + 2*betVal

        else:
            bet = 0
    else:
        if ctw > 0:
            if equityReq > ctw:
                bet = 0
            elif equityReq <= ctw + 2 and equityReq >= ctw - 2:
                bet = betVal
            elif equityReq < ctw:
                raiseCall = random.randint(1,10)
                if raiseCall > 6:
                    bet = round(0.4*(pot+betVal)) + 2*betVal
                else:
                    bet = betVal
            else:
                bet = 0
        else:
            bet = 0
    
    betSize = bet
    if betSize == 0 and betVal == 0:
        bet = 'Check'
    if betSize == 0 and betVal > 0:
        bet = 'Fold'
    if betSize > 0 and betSize == betVal:
        bet = 'Call'
    if betSize > 0 and betSize > betVal:
        bet = 'Raise'

    return bet, betSize

def equityAgent(board,pot,betVal,bHand,button,actionTaken,allIn,stack):
    betRound = len(board)

    betSize = 0
    
    if betRound == 0 and allIn == True:
        bet = anyOtherPreFlopPlay(bHand)
    elif betRound > 0 and allIn == True:
        bet = postFlopAllInDecision(bHand,board,pot,betVal)
    elif betRound == 0 and button == True and actionTaken == False:
        bet = preflopFTADecision(bHand)
    elif betRound == 0 and button == False and actionTaken == False:
        bet = preflopSTADecision(bHand,betVal)
    elif betRound == 0 and button == True and actionTaken == True:
        bet = preflop3betDecision(bHand)
    elif betRound == 0 and button == False and actionTaken == True:
        bet = anyOtherPreFlopPlay(bHand)
    elif betRound > 0 and button == False: 
        bet = postFlopFTADecision(bHand,board,pot,betVal)
    elif betRound > 0 and button == True:
        bet,betSize = postFlopResponseEquity(bHand,board,pot,betVal)

    if betSize == 0:
        if bet == 'Fold':
            betSize = 0
        elif bet == 'Check':
            betSize = 0
        elif bet == 'Call':
            betSize = betVal
        elif bet == 'Raise':
            betSize = round(0.4*(pot+betVal)) + 2*betVal
        elif bet == 'AllIn':
            betSize = stack
    
    return bet,betSize

    