import random

def randomBetGen(betVal,pot):
    decision = random.randint(1,30)

    if betVal > 0:
        if decision > 15:
            bet = 'Raise'
        else:
            bet = 'Check'
            betSize = 0
    else:
        if decision > 20:
            bet = 'Raise'
        elif decision < 11:
            bet = 'Fold'
            betSize = 0
        else:
            bet = 'Call'
            betSize = betVal
    
    if bet == 'Raise':
        betSize = random.randint(1,150)
        betSize = round((betSize/100)*(pot+betVal))
    
    return bet,betSize

def randomAgent(board,pot,betVal):
    bet,betSize = randomBetGen(betVal,pot)
    return bet,betSize
