import collections
from enum import Enum
import statistics
from itertools import groupby
from operator import itemgetter
### ----- Coordinating Hands ----- ###
def Check(board, wholeCards):
    fullHand = []
    cardNam = []
    cardVal = []
    cardMod = []
    cardVar = []
    valueList = []
    bestHand = []
    restHand = []
    restVal = []
    fullHouseList = []
    flushCheck = []
    straightCheckList = []
    straightConsec = []
    sameSuit = []
    straight = False
    flush = False
    straightFlush = False
    fullHouseCheck = False
    checkVal = False
    doubleTrips = False
    count = 0

    for i in wholeCards:
        fullHand.append(i)
    for i in board:
        fullHand.append(i)
    
    for card in fullHand:
        cardNam = card.getName()
        cardVal = int(card.getVal())
        cardMod = int(card.getMod())
        suit = cardNam[1]
        cardVar.append([cardNam, suit, cardVal, cardMod, card])
    cardVar.sort(key=lambda x: x[2])

    ### --- Flush Check --- ###
    for i in cardVar:
        flushCheck.append(i[1])
    modeSuit = statistics.mode(flushCheck)
    if flushCheck.count(modeSuit) >= 5:
        flush = True

    ### --- Mode Value --- ###
    for i in cardVar:
        valueList.append(int(i[2]))
    modeValue = statistics.mode(valueList)
    multimodeValue = statistics.multimode(valueList)
    if len(multimodeValue)>1 and valueList.count(modeValue) == 3:
        doubleTrips == True

    ### --- Straight Check ---###
    straightCheckList = list(dict.fromkeys(valueList))
    for k, g in groupby(enumerate(straightCheckList), lambda ix: ix[0]-ix[1]):
        consecList = list(map(itemgetter(1), g))
        if len(consecList) >= 5:
            straight = True
            straightConsec = consecList
        if len(consecList) == 4 and max(consecList) == 13 and valueList.count(1)>0:
            straight = True
            consecList.append(1)
            straightConsec = consecList

    
    ### --- Straight Flush Check --- ###
    if flush == True and straight == True:
        count = 0
        for i in cardVar:
            if straightConsec.count(i[2]) > 0 and i[1] == modeSuit:
                count += 1
        if count >= 5:
            straightFlush = True
                  
    ### --- Full House Check --- ###

    if valueList.count(modeValue) == 3:
        for value in valueList:
            if value != modeValue:
                fullHouseList.append(value)
        if fullHouseList.count(statistics.mode(fullHouseList)) >= 2:
            fullHouseCheck = True
        
    ### --- Declare Enumerators --- ###   8/ 
    class Hand(Enum):
        highCard = 1
        onePair = 2
        twoPair = 3
        threeKind = 4
        straight = 5
        flush = 6
        fullHouse = 7
        fourKind = 8
        straightFlush = 9
        royalFlush = 10

        @classmethod
        def getHand(self):
            return(self.value)

        
    ### --- Checks --- ###
    ### --- Royal Flush and Straight Flush --- ###
    if checkVal == False and straightFlush == True:
        bestHand = []
        count = 0

        for i in cardVar:
            if straightConsec.count(i[2]) > 0 and i[1] == modeSuit:
                bestHand.append(i[4])
        if straightConsec.count(1) > 0 and len(bestHand) == 5:
            hand = Hand.royalFlush
            checkVal = True
            print("Royal Flush")
            handString = "Royal Flush: 10 to A"
        elif len(bestHand) == 5:
            bestHand.sort(key = lambda x:x.value)
            hand = Hand.straightFlush
            print("Straight Flush")
            handString = "Straight Flush: %s to %s" %(bestHand[0].name[0], bestHand[4].name[0])
            checkVal = True

    ### --- Quads --- ###
    if checkVal == False and valueList.count(modeValue)==4:
        count = 0
        bestHand = []
        for i in cardVar:
            if i[2] == modeValue:
                count += 1
                bestHand.append(i[4])
            else:
                restHand.append(i)
        if count == 4:
            if restHand[0][2] == 1 and modeValue != 1:
                bestHand.append(restHand[0][4])
                restHand.pop(0)
                hand = Hand.fourKind
            else:
                highCard = max(restHand, key=lambda x:x[2])
                bestHand.append(highCard[4])
                hand = Hand.fourKind
            checkVal = True
            print("Quads")
            handString = "Four of a Kind: %s" %(bestHand[2].name[0])
            
    ### --- Full House --- ###
    if checkVal == False and fullHouseCheck == True:
        count = 0
        bestHand = []
        if doubleTrips == True:
            if min(multimodeValue) == 1:
                mode = 1
            else:
                mode = max(multimodeValue)
        else:
            mode = modeValue
        for i in cardVar:
            if i[2] == mode:
                bestHand.append(i[4])
            else:
                restHand.append(i)
                restVal.append(i[2])
        restMode = statistics.mode(restVal)  
        if restVal.count(restMode)>1:
            for i in restHand:
                if i[2] == restMode and len(bestHand)!=5:
                    bestHand.append(i[4])
            hand = Hand.fullHouse
            checkVal = True
            print("Full House")
            handString = "Full House: %s full of %s" %(bestHand[2].name[0], bestHand[3].name[0])


    ### --- Flush --- ###
    if checkVal == False and flush == True:
        for i in cardVar:
            if i[1] == modeSuit:
                sameSuit.append(i)
        sameSuit.sort(key=lambda x: x[2]+x[3])
        while len(sameSuit) > 5:
            sameSuit.pop(0)
        for i in sameSuit:
            bestHand.append(i[4])
        bestHand.sort(key = lambda x:x.value+x.modif, reverse = True)
        hand = Hand.flush
        checkVal = True
        print("Flush")
        handString = "%s High Flush" %(max(bestHand, key=lambda x:x.value).name[0])

    ### --- Straight --- ###
    if checkVal == False and straight == True:
        bestHand = []
        count = 0
        aceCheck = cardVar[0]
        lastChecked = cardVar[0]
        for i in cardVar:
            if straightConsec.count(i[2]) > 0:
                bestHand.append(i[4])
                straightConsec.pop(straightConsec.index(i[2]))
        if len(bestHand)> 5:
            bestHand.sort(key=lambda x:x.value)
            if max(bestHand, key = lambda x:int(x.value)) == 13 and straightCheckList.count(1) != 0:
                bestHand.sort(key = lambda x:int(x.value)+int(x.modif))
            while len(bestHand)> 5:
                bestHand.pop(0)
        if len(bestHand) == 5:
            hand = Hand.straight
            checkVal = True
            print("Straight")
            handString = "Straight: %s to %s" %(bestHand[0].name[0], bestHand[4].name[0])

    ### --- Three of a Kind --- ###
    if checkVal == False and valueList.count(modeValue) == 3 and fullHouseCheck == False:
        bestHand = []
        for card in cardVar:
            if card[2] == modeValue:
                bestHand.append(card[4])
            else:
                restHand.append(card)
        while len(bestHand) != 5:
            if restHand[0][2] == 1 and modeValue != 1:
                bestHand.append(restHand[0][4])
                restHand.pop(0)
            else:
                highCard = max(restHand, key=lambda x:x[2])
                bestHand.append(highCard[4])
                restHand.pop(restHand.index(highCard))
        hand = Hand.threeKind
        print("Three Of A Kind")
        handString = "Three of a Kind: %s" %(bestHand[2].name[0])
        checkVal = True
    ### --- Two Pair --- ###
    if checkVal == False and len(multimodeValue)>=2 and valueList.count(modeValue) == 2 :
        if len(multimodeValue)>2:
            multimodeValue.sort()
            if multimodeValue[0] == 1:
                one = multimodeValue[0]
                two = multimodeValue[2]
            else:
                one = multimodeValue[1]
                two = multimodeValue[2]
        else:
            one = multimodeValue[0]
            two = multimodeValue[1]
        for i in cardVar:
            if i[2] == one or i[2] == two:
                bestHand.append(i[4])
            else:
                restHand.append(i)
        restHand.sort(key=lambda x:x[2])
        if restHand[0][2] == 1 and modeValue != 1:
            bestHand.append(restHand[0][4])
        else:
            highCard = max(restHand, key=lambda x:x[2])
            bestHand.append(highCard[4])
        hand = Hand.twoPair
        checkVal = True
        print("Two Pair")
        handString = "Two Pair: %s and %s" %(bestHand[1].name[0], bestHand[3].name[0])
    ### --- One Pair --- ###
    if checkVal == False and len(multimodeValue) == 1 and valueList.count(modeValue) == 2:
        if valueList.count(modeValue) == 2:
            for i in cardVar:
                if i[2] == modeValue:
                    bestHand.append(i[4])
                else:
                    restHand.append(i)
            restHand.sort(key=lambda x:x[2])
            while len(bestHand) != 5:
                if restHand[0][2] == 1 and modeValue != 1:
                    bestHand.append(restHand[0][4])
                    restHand.pop(0)
                    count += 1
                else:
                    highCard = max(restHand, key=lambda x:x[2])
                    bestHand.append(highCard[4])
                    restHand.pop(restHand.index(highCard))
            hand = Hand.onePair
            checkVal = True
            print("One Pair")
            handString = "Pair of %ss" %(bestHand[1].name[0])
    ### --- High Card --- ###
    if checkVal == False:
        bestHand = []
        restHand = []
        cardVar.sort(key=lambda x:x[2])
        restHand = cardVar
        while len(bestHand) != 5:
            if restHand[0][2] == 1:
                bestHand.append(restHand[0][4])
                restHand.pop(0)
                count += 1
            else:
                highCard = max(restHand, key=lambda x:x[2])
                bestHand.append(highCard[4])
                restHand.pop(restHand.index(highCard))
                
        hand = Hand.highCard
        checkVal = True
        print("High Card")
        handString = "High Card: %s" %(max(bestHand, key=lambda x:x.value +x.modif).name[0])

    if checkVal == False:
        raise(TypeError("code not working"))
    

          #enum   array of Cards  Hand Name
    return(hand,  bestHand      , handString)
