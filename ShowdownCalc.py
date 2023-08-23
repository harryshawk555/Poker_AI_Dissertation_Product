import statistics
def ShowdownHands(aHandEnum, bHandEnum):
    if aHandEnum[0].value > bHandEnum[0].value:
        return 'a'
    elif aHandEnum[0].value < bHandEnum[0].value:
        return 'b'
    else:
        return KickerCheck(aHandEnum, bHandEnum)

def KickerCheck(aHandEnum, bHandEnum):
    valListA = []
    valListB = []
    for card in aHandEnum[1]:
        valListA.append(card.value+card.modif)
    for card in bHandEnum[1]:
        valListB.append(card.value+card.modif)
    if valListA == valListB:
        return 'chop'
    
    valListA.sort()
    valListB.sort()
    aMode = statistics.mode(valListA)
    bMode = statistics.mode(valListB)
    aMMode = statistics.multimode(valListA)
    bMMode = statistics.multimode(valListB)
    aMMode.sort(reverse=True)
    bMMode.sort(reverse=True)


    if aHandEnum[0].value == 9 or aHandEnum[0].value == 5:
        if min(valListA) == 2 and max(valListA) == 14:
            valListA = [1,2,3,4,5]
        if min(valListB) == 2 and max(valListB) == 14:
            valListB = [1,2,3,4,5]
        if max(valListA) > max(valListB):
            return 'a'
        elif max(valListA) < max(valListB):
            return 'b'
        else:
            return 'chop'
    
    if aHandEnum[0].value == 8 or aHandEnum[0].value == 7:
        if aMode > bMode:
            return 'a'
        elif aMode<bMode:
            return 'b'
        else:
            aKicker = min(valListA, key=lambda x:valListA.count(x))
            bKicker = min(valListB, key=lambda x:valListB.count(x))
            if aKicker > bKicker:
                return 'a'
            elif aKicker < bKicker:
                return 'b'
            else:
                return 'chop'
    
    if aHandEnum[0].value == 6 or aHandEnum[0].value == 1:
        for i in range(0, len(valListA)-1):
            if valListA[i] > valListB[i]:
                return 'a'
            elif valListA[i] < valListB[i]:
                return 'b'
        return 'chop'

    if aHandEnum[0].value == 2 or aHandEnum[0].value == 4:
        if aMode > bMode:
            return 'a'
        elif aMode<bMode:
            return 'b'
        else:
            valListA.sort()
            valListB.sort()
            valListA = list(dict.fromkeys(valListA))
            valListB = list(dict.fromkeys(valListB))
            valListA.pop(valListA.index(aMode))
            valListB.pop(valListB.index(aMode))
            for i in range(0, len(valListA)-1):
                if max(valListA) > max(valListB):
                    return 'a'
                elif max(valListA) < max(valListB):
                    return 'b'
                else:
                    valListA.pop(valListA.index(max(valListA)))
                    valListB.pop(valListB.index(max(valListB)))
            return 'chop'
        
    if aHandEnum[0].value == 3:
        aMMode.sort(reverse=True)
        bMMode.sort(reverse=True)
        if aMMode[0]>bMMode[0]:
            return 'a'
        elif aMMode[0]<bMMode[0]:
            return 'b'
        else:
            if aMMode[1] > bMMode[1]:
                return 'a'
            elif aMMode[1] < bMMode[1]:
                return 'b'
        aKicker = min(valListA, key=lambda x: valListA.count(x))
        bKicker = min(valListB, key=lambda x: valListB.count(x))
        if aKicker > bKicker:
            return 'a'
        elif aKicker < bKicker:
            return 'b'
        else:
            return 'chop'
