import random
from MultiCheck import HandCheck,Hand


def preflopFTADecision(hand):
    handString = []
    handVals = []
    suited = False
    pair = False
    play = 'Raise'
    for i in hand:
        handString.append(i.name)
        handVals.append(i.value + i.modif)
    if handString[0][1] == handString[1][1]:
        suited = True
    if handString[0][0] == handString[1][0]:
        pair = True
    if suited == False and pair == False:
        if min(handVals) == 4:
            if max(handVals) <=9 and max(handVals) >= 5:
                play = 'Fold'
        elif min(handVals) < 4:
            if max(handVals) <= 10:
                play = 'Fold'

    return play

def preflopSTADecision(hand, betVal):
    handString = []
    handVals = []
    suited = False
    pair = False
    play = 'Raise'
    for i in hand:
        handString.append(i.name)
        handVals.append(i.value + i.modif)
    if handString[0][1] == handString[1][1]:
        suited = True
    if handString[0][0] == handString[1][0]:
        pair = True
    if pair == False:
        if min(handVals) == 4:
            if suited == False and max(handVals) != 14:
                play = 'Fold'
            if max(handVals) > 6 and suited:
                play = 'Fold'
        elif min(handVals) < 4 and max(handVals) != 14 and suited == False:
            play = 'Fold'
        elif min(handVals) == 5:
            if suited == False and max(handVals) != 14:
                play = 'Fold'
            if max(handVals) > 7 and suited:
                play = 'Fold'
        elif min(handVals) == 6:
            if suited == False and max(handVals) != 14:
                play = 'Fold'
            if max(handVals) > 9 and suited:
                play = 'Fold'
        elif min(handVals) == 7:
            if suited == False and max(handVals) != 14:
                play = 'Fold'
            if max(handVals) > 9 and suited:
                play = 'Fold'
        elif min(handVals) == 8:
            if suited == False and max(handVals) != 14:
                play = 'Fold'
            if max(handVals) == 12 and suited:
                play = 'Fold'
        elif min(handVals) == 9:
            if max(handVals) == 11:
                play = 'Fold'

        if play == 'Fold' and betVal == 0:
            play = 'Check'
        return play
    
def preflop3betDecision(hand):
    handString = []
    handVals = []
    suited = False
    pair = False
    play = 'Fold'
    for i in hand:
        handString.append(i.name)
        handVals.append(i.value + i.modif)
    if handString[0][1] == handString[1][1]:
        suited = True
    if handString[0][0] == handString[1][0]:
        pair = True

    if pair == True and (max(handVals) > 9 or max(handVals) < 7):
        play = 'Raise'
    if pair == True and (max(handVals) <= 9 and max(handVals) >= 7):
        play = 'Call'
    
    if suited == True:
        if max(handVals) == 10 and min(handVals) == 8:
            play = 'Raise'
        if max(handVals) == 9 and (min(handVals) == 7 or min(handVals) == 6):
            play = 'Raise'
        if max(handVals) == 8 and min(handVals) == 6:
            play = 'Raise'
        if max(handVals) == 7 and min(handVals) == 5:
            play = 'Raise'
        if max(handVals) == 6 and (min(handVals) == 4 or min(handVals) == 5):
            play = 'Raise'
        if max(handVals) == 5 and min(handVals) == 4:
            play = 'Raise'
        if max(handVals) == 13 and min(handVals) >= 11:
            play = 'Raise'
        if max(handVals) == 14 and min(handVals) >= 10:
            play = 'Raise'
    elif pair == False and suited == False:
        if max(handVals) == 10 and min(handVals) == 9:
            play = 'Raise'
        if max(handVals) == 13 and min(handVals) == 12:
            play = 'Raise'
        if max(handVals) == 14 and min(handVals) >=11:
            play = 'Raise'
    

    return play

def anyOtherPreFlopPlay(hand):
    handString = []
    handVals = []
    pair = False
    for i in hand:
        handString.append(i.name)
        handVals.append(i.value + i.modif)
    if handString[0][0] == handString[1][0]:
        pair = True

    if pair == True:
        if max(handVals)>10:
            play = 'Raise'
        else:
            play = 'Call'  
    elif min(handVals) >= 11:
        play = 'Raise'
    
    else:
        play = 'Fold'

    if play == 'Fold':
        bluff = random.randint(1,100)
        if bluff > 95:
            play = 'Call'

    if play == 'Call':
        decision = random.randint(1,30)
        if decision <= 10:
            play = 'Fold'
        elif decision > 20:
            play = 'Raise'
        else:
            play = 'Call'
    
    if play == 'Raise':
        Shove = random.randint(1,40)
        if Shove > 35:
            play = 'AllIn'

    return play

### --- above is shared with equity agent --- ###

def postFlopFTADecision(hand,board,pot,betVal):
    
    #output[0] = hand
    #output[1] = bestHand
    #output[2] = handString
    #output[3] = handStrength

    fullHand = []
    valList = []
    for i in board:
        fullHand.append(i)
    for i in hand:
        fullHand.append(i)
    
    handArr = HandCheck([fullHand,hand])

    for i in handArr[1]:
        valList.append(i.value+i.modif)

    if handArr[0].value == 2:
        if handArr[3] > 40 + max(valList):
            betSize = round(0.4*pot)
            bet = 'Raise'
        else:
            betSize = betVal
            bet = 'Call'
    
    elif handArr[0].value>=3:
        betCheck = random.randint(1,10)
        if betCheck > 6:
            betSize = 0
            bet = 'Check'
        else:
            betSize = round(0.4*pot)
            bet = 'Raise'
    
    else:
        betCheck = random.randint(1,10)
        if betCheck > 9:
            betSize = round(0.4*pot)
            bet = 'Raise'
        else:
            betSize = 0
            bet = 'Check'

    return bet, betSize

def postFlopResponseDecision(hand,board,pot,betVal):
    
    #output[0] = hand
    #output[1] = bestHand
    #output[2] = handString
    #output[3] = handStrength

    fullHand = []
    valList = []
    for i in board:
        fullHand.append(i)
    for i in hand:
        fullHand.append(i)
    
    handArr = HandCheck([fullHand,hand])

    for i in handArr[1]:
        valList.append(i.value+i.modif)

    if handArr[0].value == 2 and  handArr[3] > 40 + max(valList):
        betCall = random.randint(1,12)
        if betCall > 9:
            betSize = round(0.4*(pot+betVal)) + 2*betVal
            bet = 'Raise'
        elif betCall < 3:
            betSize = 0
            bet = 'Fold'
        else:
            betSize = betVal
            bet = 'Call'
    
    elif handArr[0].value>=3:
        betCheck = random.randint(1,10)
        if betCheck > 8:
            betSize = 0
            bet = 'Fold'
        elif betCheck <3:
            betSize = betVal
            bet = 'Call'
        else:
            betSize = round(0.4*(pot+betVal)) + 2*betVal
            bet = 'Raise'
    
    else:
        betCheck = random.randint(1,30)
        if betCheck > 27:
            betSize = round(0.4*(pot+betVal)) + 2*betVal
            bet = 'Raise'
        elif betCheck == 19:
            betSize = round(1.25*(pot+betVal))
            bet = 'Raise'
        else:
            betSize = 0
            bet = 'Fold'

    return bet, betSize


def postFlopAllInDecision(hand,board,pot,betVal):
    
    #output[0] = hand
    #output[1] = bestHand
    #output[2] = handString
    #output[3] = handStrength

    fullHand = []
    valList = []
    for i in board:
        fullHand.append(i)
    for i in hand:
        fullHand.append(i)
    
    handArr = HandCheck([fullHand,hand])

    for i in handArr[1]:
        valList.append(i.value+i.modif)

    if handArr[0].value == 2 and  handArr[3] > 40 + max(valList):
        betCall = random.randint(1,12)
        if betCall < 5:
            bet = 'Fold'
            betSize = 0
        else:
            bet = 'AllIn'
            betSize = betVal
    
    elif handArr[0].value>=3:
        betCheck = random.randint(1,10)
        if betCheck > 7:
            bet = 'Fold'
            betSize = 0
        else:
            bet = 'AllIn'
            betSize = betVal
    
    else:
        betCheck = random.randint(1,30)
        if betCheck == 19 and max(hand, key=lambda i: i.value+i.modif)>13:
            bet = 'AllIn'
            betSize = betVal
        else:
            bet = 'Fold'
            betSize = 0

    return bet, betSize


def gtoAgent(board,pot,betVal,bHand,button,actionTaken,allIn,stack):
    betRound = len(board)

    betSize = ''
    
    if betRound == 0 and allIn == True:
        bet = anyOtherPreFlopPlay(bHand)
    elif betRound > 0 and allIn == True:
        bet, betSize = postFlopAllInDecision(bHand,board,pot,betVal)
    elif betRound == 0 and button == True and actionTaken == False:
        bet = preflopFTADecision(bHand,board,pot,betVal)
    elif betRound == 0 and button == False and actionTaken == False:
        bet = preflopSTADecision(bHand, betVal)
    elif betRound == 0 and button == True and actionTaken == True:
        bet = preflop3betDecision(bHand)
    elif betRound == 0 and button == False and actionTaken == True:
        bet = anyOtherPreFlopPlay(bHand)
    elif betRound > 0 and button == False: 
        bet,betSize = postFlopFTADecision(bHand,board,pot,betVal)
    elif betRound > 0 and button == True:
        bet,betSize = postFlopResponseDecision(bHand,board,pot,betVal)


    if betSize == '':
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
        else:
            bet = 'Fold'
            betSize = 0
    
    if betSize > stack:
        betSize = stack
        bet = 'AllIn'
    
    return bet,betSize