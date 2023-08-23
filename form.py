from tkinter import *
from tkinter import ttk
import time
from handCheck import Check
from initialize import Initialize
from ShowdownCalc import *
from post_train_agent import *
import random
from PIL import Image,ImageTk

def InitPTable():
    global BetBox
    global abetbutt
    global acall
    global check
    global afold
    global bbetbutt
    global bcall
    global bfold
    global preFlopScores
    BetBox = StringVar()
    Ai_Agent = Init_AI_Agent()
    Deck = Initialize()
    preFlopScores = handRankAiCalcsPreFlop(Deck)

    

    def reset():
        global canvas
        global root
        global bg
        global button
        global aStack
        global bStack
        global aHand
        global bHand
        global board
        global wIm1
        global wIm2
        global bIm1
        global bIm2
        global bIm3
        global bIm4
        global bIm5
        global pbIm1
        global pbIm2
        global betDiff
        global aCurrBet
        global bCurrBet
        global BetBox
        global button
        global pot
        global board
        global currentBoard
        global wholeCards
        global aHandEnum
        global bHandEnum
        global action
        global rObet
        global abetbutt
        global acall
        global check
        global afold
        global bbetbutt
        global bcall
        global bfold
        global actionTaken
        global AllIn
        global preFlopScores

        AllIn = False

        if aStack == 0:
            aStack = 250
        
        if bStack == 0:
            bStack = 250

        actionTaken = False
        board = []
        currentBoard = []
        wholeCards = []
        aHandEnum = []
        bHandEnum = []
        betDiff = 2
        pot = 0

        if button == True:
            aCurrBet = 1
            bCurrBet = 2

        else:
            aCurrBet = 2
            bCurrBet = 1
        aStack -= aCurrBet
        bStack -= bCurrBet
        betDiff = 0
        board = random.sample(Deck, 12)
        aHand = [board[0], board[2]]
        bHand = [board[1], board[3]]
        board.pop(0)
        board.pop(0)
        board.pop(0)
        board.pop(0)

        for card in aHand:
            card.setImage()
        for card in bHand:
            card.setImage()
        for card in board:
            card.setImage()
        
        pbIm1 = ImageTk.PhotoImage(bHand[0].getImage())
        pbIm2 = ImageTk.PhotoImage(bHand[1].getImage())
        pbIm1.img = pbIm1
        pbIm2.img = pbIm2
        wIm1 = ImageTk.PhotoImage(aHand[0].getImage())
        wIm2 = ImageTk.PhotoImage(aHand[1].getImage())
        bIm1 = ImageTk.PhotoImage(board[0].getImage())
        bIm2 = ImageTk.PhotoImage(board[1].getImage())
        bIm3 = ImageTk.PhotoImage(board[2].getImage())
        bIm4 = ImageTk.PhotoImage(board[4].getImage())  
        bIm5 = ImageTk.PhotoImage(board[6].getImage())
        bIm1.image = bIm1
        bIm2.image = bIm2
        bIm3.image = bIm3
        bIm4.image = bIm4
        bIm5.image = bIm5
        nTSize = []
        table = Image.open('Images/pokerTable.png')
        tSize = table.size
        for i in tSize:
            nTSize.append(round(i*1.2))
        newTable = table.resize(tuple((nTSize[0],nTSize[1])))
        bg = ImageTk.PhotoImage(newTable)
        buttonIm = Image.open('Images/dealerButton.png')
        buttonIm = buttonIm.resize((50,50))
        butIm = ImageTk.PhotoImage(buttonIm)
        butIm.image = butIm
        canvas.create_image(100,90,anchor=NW,image=bg)


        if button == True:
            canvas.create_image(600,360,anchor=NW,image=butIm,tag='button')
        else:
            canvas.create_image(600,160,anchor=NW,image=butIm,tag='button')

        canvas.create_image(415,410,anchor=NW,image=wIm1,tag='aHand')
        canvas.create_image(487,410,anchor=NW,image=wIm2,tag='aHand')
        canvas.create_text(487,400,anchor=CENTER, text=aCurrBet, tag = 'aBets')
        canvas.create_text(487,208,anchor=CENTER, text=bCurrBet, tag = 'bBets')
        canvas.create_text(270,307,anchor=CENTER, text=0, tag = 'pot')
        canvas.create_text(387,458,anchor=CENTER, text='£'+str(int(aStack)),tag='aStack')
        canvas.create_text(387,158,anchor=CENTER, text='£'+str(int(bStack)),tag='bStack')

        action = button
        rObet = 0


        canvas.create_window(487,460,window=BetBoxEntry)
        if action == True:  
            if int(bCurrBet) == int(aCurrBet) or (bCurrBet == 0 and int(aCurrBet) == 0):
                canvas.create_window(537,480,window=check,tag='a')
            else:
                canvas.create_window(537,480,window=acall,tag='a')
            canvas.create_window(537,500,window=afold,tag='a')
            canvas.create_window(537,460,window=abetbutt,tag='a')
            if bStack != 0 and aStack !=0:
                canvas.create_window(597,460,window=aallin,tag='a')
            canvas.create_text(428,228,text='Player A To Act',tag='a')
        else:
            absVal = preFlopScores[findAbsVal(preFlopScores, bHand)]
            ai_bet, ai_size = ai_decision_test(Ai_Agent, int(pot)+int(aCurrBet)+int(bCurrBet), max( [int(aCurrBet),int(bCurrBet)]),
                                                bStack, absVal)
            if type(ai_bet) is tuple:
                ai_size = ai_bet[1]
                ai_bet = ai_bet[0]
            
            if ai_bet == 'Check' and aCurrBet != bCurrBet:
                ai_bet = 'Fold'

            if ai_bet == 'Call' and aCurrBet == bCurrBet:
                ai_bet = 'Check'

            if ai_bet == 'Fold':
                bFold()
            elif ai_bet == 'Check':
                confAction()
            elif ai_bet == 'Call':
                bCall(ai_size)
            elif ai_bet == 'Raise':
                bBet(ai_size)
            elif ai_bet == 'AllIn':
                bAllIn()



    def dealFlop():
        global currentBoard
        currentBoard = [board[0],board[1],board[2]]

        global bIm1
        global bIm2
        global bIm3
        global rObet
        global action
        global pot
        global aStack
        global bStack
        global bCurrBet
        global aCurrBet
        global actionTaken
        global preFlopScores
        global postFlopScores
        global AllIn

        actionTaken = False
        postFlopScores = handRankAiCalcsPostFlop(currentBoard,Deck)
        canvas.delete('aBets')
        canvas.create_text(487,400,anchor=CENTER, text=0, tag = 'aBets')
        canvas.delete('bBets')
        canvas.create_text(487,208,anchor=CENTER, text=0, tag = 'bBets')

        pot = pot + int(aCurrBet) + int(bCurrBet)
        canvas.delete('pot')
        canvas.delete('b')
        canvas.delete('a')
        canvas.create_text(270,307,anchor=CENTER, text=pot, tag = 'pot')

        aCurrBet = 0
        bCurrBet = 0

        bIm1 = ImageTk.PhotoImage(board[0].getImage())
        bIm2 = ImageTk.PhotoImage(board[1].getImage())
        bIm3 = ImageTk.PhotoImage(board[2].getImage())
        currentHand()
        canvas.create_image(307,250,anchor=NW,image=bIm1,tag='flop')
        canvas.create_image(379,250,anchor=NW,image=bIm2,tag='flop')
        canvas.create_image(451,250,anchor=NW,image=bIm3,tag='flop')
        if aStack == 0 or bStack == 0:
            AllIn == True
            confAction()
        rObet=1
        if action == True:  
            if int(bCurrBet) == int(aCurrBet) or (int(bCurrBet) == 0 and int(aCurrBet) == 0):
                canvas.create_window(537,480,window=check,tag='a')
            else:
                canvas.create_window(537,480,window=acall,tag='a')
            canvas.create_window(537,500,window=afold,tag='a')
            canvas.create_window(537,460,window=abetbutt,tag='a')
            if bStack != 0 and aStack !=0:
                canvas.create_window(597,460,window=aallin,tag='a')
            canvas.create_text(428,228,text='Player A To Act',tag='a')
        else:
            time.sleep(1)
            absVal = postFlopScores[findAbsVal(postFlopScores, bHand)]
            ai_bet, ai_size = ai_decision_test(Ai_Agent, int(pot)+int(aCurrBet)+int(bCurrBet), max( [int(aCurrBet),int(bCurrBet)]),
                                                bStack, absVal)
            if type(ai_bet) is tuple:
                ai_size = ai_bet[1]
                ai_bet = ai_bet[0]
            
            if ai_bet == 'Check' and int(aCurrBet) > 0:
                ai_bet = 'Fold'

            if ai_bet == 'Call' and int(aCurrBet) == bCurrBet:
                ai_bet = 'Check'

            if ai_bet == 'Fold':
                bFold()
            elif ai_bet == 'Check':
                confAction()
            elif ai_bet == 'Call':
                bCall(ai_size)
            elif ai_bet == 'Raise':
                bBet(ai_size)
            elif ai_bet == 'AllIn':
                bAllIn()
        canvas.update()

    
    def dealTurn():
        global currentBoard
        global bIm4
        global rObet
        global pot
        global action
        global aStack
        global bStack
        global bCurrBet
        global aCurrBet
        global actionTaken
        global postFlopScores
        global AllIn

        actionTaken = False

        currentBoard.append(board[4])
        currentHand()

        postFlopScores = handRankAiCalcsPostFlop(currentBoard,Deck)
        bIm4 = ImageTk.PhotoImage(board[4].getImage())
        canvas.create_image(523,250,anchor=NW,image=bIm4,tag='turn')
        rObet=2

        pot = pot + int(aCurrBet) + int(bCurrBet)

        canvas.delete('aBets')
        canvas.create_text(487,400,anchor=CENTER, text=0, tag = 'aBets')
        canvas.delete('bBets')
        canvas.create_text(487,208,anchor=CENTER, text=0, tag = 'bBets')

        canvas.delete('pot')
        canvas.delete('b')
        canvas.delete('a')
        canvas.create_text(270,307,anchor=CENTER, text=pot, tag = 'pot')

        aCurrBet = 0
        bCurrBet = 0

        canvas.create_text(387,158,anchor=CENTER, text='£'+str(bStack),tag='bStack')
        canvas.create_text(387,458,anchor=CENTER, text='£'+str(aStack),tag='aStack')

        if aStack == 0 or bStack == 0:
            AllIn == True
            confAction()

        if action == True:  
            if int(bCurrBet) == int(aCurrBet) or (int(bCurrBet) == 0 and int(aCurrBet) == 0):
                canvas.create_window(537,480,window=check,tag='a')
            else:
                canvas.create_window(537,480,window=acall,tag='a')
            canvas.create_window(537,500,window=afold,tag='a')
            canvas.create_window(537,460,window=abetbutt,tag='a')
            canvas.create_window(597,460,window=aallin,tag='a')
            canvas.create_text(428,228,text='Player A To Act',tag='a')
        else:
            time.sleep(1)
            absVal = postFlopScores[findAbsVal(postFlopScores, bHand)]
            ai_bet, ai_size = ai_decision_test(Ai_Agent, int(pot)+int(aCurrBet)+int(bCurrBet), max( [int(aCurrBet),int(bCurrBet)]),
                                                bStack, absVal)
            if type(ai_bet) is tuple:
                ai_size = ai_bet[1]
                ai_bet = ai_bet[0]
            
            if ai_bet == 'Check' and int(aCurrBet) > 0:
                ai_bet = 'Fold'

            if ai_bet == 'Call' and int(aCurrBet) == bCurrBet:
                ai_bet = 'Check'

            if ai_bet == 'Fold':
                bFold()
            elif ai_bet == 'Check':
                confAction()
            elif ai_bet == 'Call':
                bCall(ai_size)
            elif ai_bet == 'Raise':
                bBet(ai_size)
            elif ai_bet == 'AllIn':
                bAllIn()
        canvas.update()

    def dealRiver():
        global bIm5
        global aHandEnum
        global currentBoard
        global rObet
        global action
        global pot
        global aStack
        global bStack
        global bCurrBet
        global aCurrBet
        global actionTaken
        global postFlopScores

        actionTaken = False

        currentBoard.append(board[6])
        currentHand()

        postFlopScores = handRankAiCalcsPostFlop(currentBoard,Deck)
        bIm5 = ImageTk.PhotoImage(board[6].getImage())
        canvas.create_image(595,250,anchor=NW,image=bIm5,tag='river')
        rObet = 3
        canvas.delete('aStack')
        canvas.delete('bStack')

        canvas.delete('aBets')
        canvas.create_text(487,400,anchor=CENTER, text=0, tag = 'aBets')
        canvas.delete('bBets')
        canvas.create_text(487,208,anchor=CENTER, text=0, tag = 'bBets')

        pot = pot + int(aCurrBet) + int(bCurrBet)
        canvas.delete('pot')
        canvas.delete('b')
        canvas.delete('a')
        canvas.create_text(270,307,anchor=CENTER, text=pot, tag = 'pot')

        aCurrBet = 0
        bCurrBet = 0
        
        canvas.create_text(387,158,anchor=CENTER, text='£'+str(bStack),tag='bStack')
        canvas.create_text(387,458,anchor=CENTER, text='£'+str(aStack),tag='aStack')

        if aStack == 0 or bStack == 0:
            AllIn == True
            confAction()
        if action == True:  
            if int(bCurrBet) == int(aCurrBet) or (int(bCurrBet) == 0 and int(aCurrBet) == 0):
                canvas.create_window(537,480,window=check,tag='a')
            else:
                canvas.create_window(537,480,window=acall,tag='a')
            canvas.create_window(537,500,window=afold,tag='a')
            canvas.create_window(537,460,window=abetbutt,tag='a')
            if bStack != 0 and aStack !=0:
                canvas.create_window(597,460,window=aallin,tag='a')
            canvas.create_text(428,228,text='Player A To Act',tag='a')
        else:
            time.sleep(1)
            absVal = postFlopScores[findAbsVal(postFlopScores, bHand)]
            ai_bet, ai_size = ai_decision_test(Ai_Agent, int(pot)+int(aCurrBet)+int(bCurrBet), max( [int(aCurrBet),int(bCurrBet)]),
                                                bStack, absVal)
            if type(ai_bet) is tuple:
                ai_size = ai_bet[1]
                ai_bet = ai_bet[0]
            
            if ai_bet == 'Check' and int(aCurrBet) > 0:
                ai_bet = 'Fold'

            if ai_bet == 'Call' and int(aCurrBet) == bCurrBet:
                ai_bet = 'Check'

            if ai_bet == 'Fold':
                bFold()
            elif ai_bet == 'Check':
                confAction()
            elif ai_bet == 'Call':
                bCall(ai_size)
            elif ai_bet == 'Raise':
                bBet(ai_size)
            elif ai_bet == 'AllIn':
                bAllIn()
        canvas.update()

    def dealShowdown():
        global canvas
        global pbIm1
        global pbIm2
        global aHandEnum
        global bHandEnum
        global button
        global aStack
        global bStack
        global bCurrBet
        global aCurrBet
        global pot
        currentHandb()

        pot += int(aCurrBet) + int(bCurrBet)
        print(pot)
        aCurrBet = 0
        bCurrBet = 0
        result = ShowdownHands(aHandEnum, bHandEnum)
        if result == 'a':
            aStack += pot
            if pot > round(0.75*250):
                Ai_Agent.learn(0)
            else:
                Ai_Agent.learn(1)
        elif result == 'b':
            bStack += pot
            if pot > round(0.75*250):
                Ai_Agent.learn(3)
            else:
                Ai_Agent.learn(2)
        elif result == 'chop':
            pot = pot/2
            aStack += pot
            bStack += pot 
            Ai_Agent.learn(2)          
        button = not(button)
        print(result)
        showBHand()
        deleteLoop()
        reset()

    def Runout():
        global canvas
        global button
        global bCurrBet
        global aCurrBet
        global pot
        global bIm1
        global bIm2
        global bIm3
        global bIm4
        global bIm5
        global board
        global currentBoard
        currentBoard = []

        pot = pot + int(aCurrBet) + int(bCurrBet)

        canvas.delete('aBets')
        canvas.create_text(487,400,anchor=CENTER, text=0, tag = 'aBets')
        canvas.delete('bBets')
        canvas.create_text(487,208,anchor=CENTER, text=0, tag = 'bBets')

        canvas.delete('pot')
        canvas.delete('b')
        canvas.delete('a')
        canvas.create_text(270,307,anchor=CENTER, text=pot, tag = 'pot')

        aCurrBet = 0
        bCurrBet = 0

        canvas.delete('flop')
        canvas.delete('turn')
        canvas.delete('river')

        canvas.create_image(307,250,anchor=NW,image=bIm1,tag='flop')
        canvas.create_image(379,250,anchor=NW,image=bIm2,tag='flop')
        canvas.create_image(451,250,anchor=NW,image=bIm3,tag='flop')
        canvas.create_image(523,250,anchor=NW,image=bIm4,tag='turn')
        canvas.create_image(595,250,anchor=NW,image=bIm5,tag='river')

        currentBoard.append(board[0])
        currentBoard.append(board[1])
        currentBoard.append(board[2])
        currentBoard.append(board[4])
        currentBoard.append(board[6])

        currentHand()

        canvas.update()




        

    def currentHand():
        global aHandEnum
        canvas.delete('handStrength')
        aHandEnum = Check(currentBoard, aHand)
        canvas.create_text(487,530,anchor=CENTER, text=aHandEnum[2], tag = 'handStrength')

    def currentHandb():
        global bHandEnum
        canvas.delete('bHandStrength')
        bHandEnum = Check(currentBoard, bHand)
        canvas.create_text(487,80,anchor=CENTER, text=bHandEnum[2], tag = 'bHandStrength')

    def aBet(bet):
        global canvas
        global betDiff
        global bCurrBet
        global aCurrBet
        global bStack
        global aStack
        global action
        global actionTaken
        global abetbutt
        global acall
        global check
        global afold
        global bbetbutt
        global bcall
        global bfold
        global AllIn
        global preFlopScores
        global postFlopScores
        action = not(action)
        BetBoxEntry.delete(0,END)

        if bet == bCurrBet:
            actionTaken = True

        if int(aStack) + int(aCurrBet) >= int(bStack) + int(bCurrBet):
            smallStack = int(bStack) + int(bCurrBet)
        else:
            smallStack = int(aStack) + int(aCurrBet)
        
        if int(bet) >= smallStack or aStack == 0 or bStack == 0:
            bet = smallStack 
            AllIn = True   

        if (int(bet) >= int(betDiff) + int(bCurrBet)) or (int(bet) == int(bCurrBet)):
            aStack += int(aCurrBet)
            canvas.delete('a')
            canvas.delete('b')
            betDiff = int(bet) - int(bCurrBet)
            canvas.delete('aBets')
            canvas.delete('aStack')
            aCurrBet = bet
            aStack -= int(bet)
            canvas.create_text(487,400,anchor=CENTER, text=bet, tag = 'aBets')
            canvas.create_text(387,458,anchor=CENTER, text='£'+str(aStack),tag='aStack')
            time.sleep(1)
            if actionTaken == False:
                if rObet == 0:
                    absVal = preFlopScores[findAbsVal(preFlopScores, bHand)]
                else: 
                    absVal = postFlopScores[findAbsVal(postFlopScores, bHand)]
                ai_bet, ai_size = ai_decision_test(Ai_Agent, int(pot)+int(aCurrBet)+int(bCurrBet), max( [int(aCurrBet),int(bCurrBet)]),
                                                    bStack, absVal)
                if type(ai_bet) is tuple:
                    ai_size = ai_bet[1]
                    ai_bet = ai_bet[0]
                
                if ai_bet == 'Check' and aCurrBet > 0:
                    ai_bet = 'Fold'

                if ai_bet == 'Call' and aCurrBet == bCurrBet:
                    ai_bet = 'Check'

                if ai_bet == 'Fold':
                    bFold()
                elif ai_bet == 'Check':
                    confAction()
                elif ai_bet == 'Call':
                    bCall(ai_size)
                elif ai_bet == 'Raise':
                    bBet(ai_size)
                elif ai_bet == 'AllIn':
                    bAllIn()
            else: confAction()

            

    
    def bBet(bet):
        global canvas
        global betDiff
        global bCurrBet
        global aCurrBet
        global bStack
        global aStack
        global action
        global actionTaken
        global abetbutt
        global acall
        global check
        global afold
        global bbetbutt
        global bcall
        global bfold
        global AllIn
        action = not(action)
        BetBoxEntry.delete(0,END)

        if bet == aCurrBet:
            actionTaken = True

        if int(aStack) + int(aCurrBet) >= int(bStack) + int(bCurrBet):
            smallStack = int(bStack) + int(bCurrBet)
        else:
            smallStack = int(aStack) + int(aCurrBet)
        
        if int(bet) >= smallStack or aStack == 0 or bStack == 0:
            bet = smallStack
            AllIn = True
        
        if (int(bet) >= int(betDiff) + int(aCurrBet)) or (int(bet) == int(aCurrBet)):
            bStack += int(bCurrBet)
            betDiff = int(bet) - int(aCurrBet)
            canvas.delete('bBets')
            canvas.delete('bStack')
            bStack -= int(bet)
            bCurrBet = int(bet)
            canvas.create_text(487,208,anchor=CENTER, text=bet, tag = 'bBets')
            canvas.create_text(387,158,anchor=CENTER, text='£'+str(bStack),tag='bStack')
            canvas.delete('b')
            if int(bCurrBet) == int(aCurrBet) or (int(bCurrBet) == 0 and int(aCurrBet) == 0):
                canvas.create_window(537,480,window=check,tag='a')
            else:
                canvas.create_window(537,480,window=acall,tag='a')
            canvas.create_window(537,500,window=afold,tag='a')
            canvas.create_window(537,460,window=abetbutt,tag='a')
            if bStack != 0 and aStack !=0:
                canvas.create_window(597,460,window=aallin,tag='a')
            canvas.create_text(428,228,text='Player A To Act',tag='a')

    def aCall(bet):
        global canvas
        global rObet
        global button
        global action
        global actionTaken
        global aStack
        global bStack
        global aCurrBet
        global bCurrBet
        global AllIn
        print(AllIn)
      
        if AllIn == True:
            aBet(bet)
            Runout()
            dealShowdown()
        else:    
            if rObet == 0 and actionTaken == True and AllIn == False:
                action = not(button)
                aBet(bet)
                dealFlop()
            elif rObet == 1 and actionTaken == True and AllIn == False:
                aBet(bet)
                dealTurn()
            elif rObet == 2 and actionTaken == True and AllIn == False:
                aBet(bet)
                dealRiver()
            elif rObet == 3 and actionTaken == True and AllIn == False:
                aBet(bet)
                dealShowdown()
            else:
                actionTaken = True
                aBet(bet)
                

    def bCall(bet):
        global canvas
        global rObet
        global button
        global action
        global actionTaken
        global aStack
        global bStack
        global aCurrBet
        global AllIn
        print(AllIn)

        if AllIn == True:
            bBet(bet)
            Runout()
            dealShowdown()
        else:
            if rObet == 0 and actionTaken == True and AllIn == False:
                action = not(button)
                bBet(bet)
                dealFlop()
            elif rObet == 1 and actionTaken == True and AllIn == False:
                bBet(bet)
                dealTurn()
            elif rObet == 2 and actionTaken == True and AllIn == False:
                bBet(bet)
                dealRiver()
            elif rObet == 3 and actionTaken == True and AllIn == False:
                bBet(bet)
                dealShowdown()
            else:
                bBet(bet)
                actionTaken = True


    def bFold():
        global canvas
        global bHand
        global bCurrBet
        global aCurrBet
        global aStack
        global bStack
        global button
        global pot
        showBHand()
        pot += int(bCurrBet) + int(aCurrBet)
        aStack += int(pot)
        button = not(button)
        deleteLoop()
        if pot > round(0.75*250):
            Ai_Agent.learn(0)
        else:
            Ai_Agent.learn(1)
        reset()

    def aFold():
        global canvas
        global pbIm1
        global pbIm2
        global bHand
        global bStack
        global aStack
        global bCurrBet
        global aCurrBet
        global button
        global pot
        showBHand()
        pot += int(aCurrBet) + int(bCurrBet)
        bStack += pot
        button = not(button)
        deleteLoop()
        if pot > round(0.75*250):
            Ai_Agent.learn(2)
        else:
            Ai_Agent.learn(3)
        reset()

    def aAllIn():
        global canvas
        global rObet
        global betDiff
        global bCurrBet
        global aCurrBet
        global aStack
        global action
        global actionTaken
        global abetbutt
        global acall
        global check
        global afold
        global bbetbutt
        global bcall
        global bfold
        global AllIn

        AllIn = True
        action = not(action)
        BetBoxEntry.delete(0,END)

        if int(aStack) + int(aCurrBet) >= int(bStack) + int(bCurrBet):
            smallStack = int(bStack) + int(bCurrBet)
        else:
            smallStack = int(aStack) + int(aCurrBet)
        
        aStack += int(aCurrBet)
        canvas.delete('a')
        canvas.delete('b')
        betDiff = int(smallStack) - int(bCurrBet)
        canvas.delete('aBets')
        canvas.delete('aStack')
        aCurrBet = smallStack
        aStack -= int(smallStack)
        canvas.create_text(487,400,anchor=CENTER, text=smallStack, tag = 'aBets')
        canvas.create_text(387,458,anchor=CENTER, text='£'+str(aStack),tag='aStack')
        time.sleep(1)
        if rObet == 0:
            absVal = preFlopScores[findAbsVal(preFlopScores, bHand)]
        else:
            absVal = postFlopScores[findAbsVal(postFlopScores, aHand)]
        ai_bet, ai_size = ai_decision_test(Ai_Agent, int(pot)+int(aCurrBet)+int(bCurrBet), max( [int(aCurrBet),int(bCurrBet)]),
                                            bStack, absVal)
        if type(ai_bet) is tuple:
            ai_size = ai_bet[1]
            ai_bet = ai_bet[0]
        
        if ai_bet == 'Check' and aCurrBet > 0:
            ai_bet = 'Fold'

        if ai_bet == 'Call' and aCurrBet == bCurrBet:
            ai_bet = 'Check'

        if ai_bet == 'Fold':
            bFold()
        elif ai_bet == 'Call':
            bCall(ai_size)
        elif ai_bet == 'Raise':
            bCall(aCurrBet)
        elif ai_bet == 'AllIn':
            bCall(aCurrBet)


    def bAllIn():

        global canvas
        global betDiff
        global aCurrBet
        global bCurrBet
        global bStack
        global check
        global action
        global actionTaken
        global abetbutt
        global acall
        global check
        global afold
        global bbetbutt
        global bcall
        global bfold
        global AllIn

        AllIn == True
        action = not(action)
        BetBoxEntry.delete(0,END)
        actionTaken = True

        if int(aStack) + int(aCurrBet) >= int(bStack) + int(bCurrBet):
            smallStack = int(bStack) + int(bCurrBet)
        else:
            smallStack = int(aStack) + int(aCurrBet)

        bStack += int(bCurrBet)
        betDiff = int(smallStack) - int(aCurrBet)
        canvas.delete('bBets')
        canvas.delete('bStack')
        bStack -= int(smallStack)
        bCurrBet = int(smallStack)
        canvas.create_text(487,208,anchor=CENTER, text=smallStack, tag = 'bBets')
        canvas.create_text(387,158,anchor=CENTER, text='£'+str(bStack),tag='bStack')
        canvas.delete('b')
        if int(bCurrBet) == int(aCurrBet) or (int(bCurrBet) == 0 and int(aCurrBet) == 0):
            canvas.create_window(537,480,window=check,tag='a')
        else:
            canvas.create_window(537,480,window=acall,tag='a')
        canvas.create_window(537,500,window=afold,tag='a')
        canvas.create_window(537,460,window=abetbutt,tag='a')
        if AllIn == False:
                canvas.create_window(597,460,window=aallin,tag='a')
        canvas.create_text(428,228,text='Player A To Act',tag='a')

    def confAction():
        global abetbutt
        global bbetbutt
        global rObet
        global BetBox
        global acall
        global bcall
        global check
        global afold
        global bfold
        global button
        global action
        global aCurrBet
        global bCurrBet
        global actionTaken
        global AllIn
        global postFlopScores
        global preFlopScores

        action = not(action)

        if AllIn == True:
            Runout()
            dealShowdown()

        if rObet == 0 and actionTaken == True:
            action = not(button)
            dealFlop()
        elif rObet == 1 and actionTaken == True:
            dealTurn()
        elif rObet == 2 and actionTaken == True:
            dealRiver()
        elif rObet == 3 and actionTaken == True:
            dealShowdown()
        else:  
            canvas.delete('a')
            canvas.delete('b')
            BetBoxEntry.delete(0,END)
            if action == True:  
                if int(bCurrBet) == int(aCurrBet) or (int(bCurrBet) == 0 and int(aCurrBet) == 0):
                    canvas.create_window(537,480,window=check,tag='a')
                else:
                    canvas.create_window(537,480,window=acall,tag='a')
                canvas.create_window(537,500,window=afold,tag='a')
                canvas.create_window(537,460,window=abetbutt,tag='a')
                if bStack != 0:
                    canvas.create_window(597,460,window=aallin,tag='a')
                canvas.create_text(428,228,text='Player A To Act',tag='a')
            else:
                time.sleep(1)
                if rObet == 0:
                    absVal = preFlopScores[findAbsVal(preFlopScores, bHand)]
                else:
                    absVal = postFlopScores[findAbsVal(postFlopScores, aHand)]
                ai_bet, ai_size = ai_decision_test(Ai_Agent, int(pot)+int(aCurrBet)+int(bCurrBet), max( [int(aCurrBet),int(bCurrBet)]),
                                                    bStack, absVal)
                if type(ai_bet) is tuple:
                    ai_size = ai_bet[1]
                    ai_bet = ai_bet[0]
                
                if ai_bet == 'Check' and aCurrBet != bCurrBet:
                    ai_bet = 'Fold'

                if ai_bet == 'Call' and aCurrBet == bCurrBet:
                    ai_bet = 'Check'

                if ai_bet == 'Fold':
                    bFold()
                elif ai_bet == 'Check':
                    confAction()
                elif ai_bet == 'Call':
                    bCall(ai_size)
                elif ai_bet == 'Raise':
                    bBet(ai_size)
                elif ai_bet == 'AllIn':
                    bAllIn()
            actionTaken = True


    def deleteLoop():
        canvas.delete(ALL)

    def showBHand():
        global pbIm1
        global pbIm2

        canvas.create_image(415,90,anchor=NW,image=pbIm1,tag='bHand')
        canvas.create_image(487,90,anchor=NW,image=pbIm2,tag='bHand')
        root.update()
        time.sleep(4)

    BetBoxEntry=ttk.Entry(root,textvariable=BetBox)
    check = ttk.Button(root,text='Check',command=lambda: confAction())
    acall = ttk.Button(root,text='Call',command=lambda:aCall(int(bCurrBet)))
    afold = ttk.Button(root,text='Fold',command=lambda:aFold())
    abetbutt = ttk.Button(root,text='A: bet',command=lambda: aBet(BetBox.get()))
    aallin = ttk.Button(root,text='All In',command=lambda:aAllIn())
    bcall = ttk.Button(root,text='Call',command=lambda:bCall(int(aCurrBet)))
    bfold = ttk.Button(root,text='Fold',command=lambda:bFold())
    bbetbutt = ttk.Button(root,text='B: bet',command=lambda: bBet(BetBox.get()))
    ballin = ttk.Button(root,text='All In',command=lambda:bAllIn())

    reset()

global bg
global aStack
global bStack
global button

button = False
aStack = 250
bStack = 250

root = Tk()
root.title('Poker Form')
root.geometry('974x800')

canvas = Canvas(root, width=974, height=550)
canvas.pack()

InitPTable()

root.mainloop()

