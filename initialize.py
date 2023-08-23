from PIL import Image,ImageTk
### ----- initializing the deck ----- ###
def Initialize():
    global Deck
    global Card
    Cards = ["2","3","4","5","6","7","8","9","T","J","Q","K","A"]
    Suits = ["h","c","d","s"]
    Deck = []
    

    print("Initialize running")
    class Card:
        value = 0
        name = ""
        modif = 0
        image = ''
        deck = []
        
        def __init__(self, value, name, modif):
            self.value = int(value)
            self.name = name
            self.modif = int(modif)
            
        def getName(self):
            name = self.name
            return name
        def getVal(self):
            value = self.value
            return value
        def getMod(self):
            modif = self.modif
            return modif
        def setImage(self):
            val = self.value
            suit = self.name[1]
            tupleSet = []
            if suit == 'h':
                suitHeightTop = 38
            elif suit == 'd':
                suitHeightTop = 181
            elif suit == 'c':
                suitHeightTop = 324
            elif suit == 's':
                suitHeightTop = 467
            suitHeightBottom = suitHeightTop + 135

            cardWidthEnd = 98*val-1
            cardWidthStart = cardWidthEnd-90
            
            im = Image.open("Images/cards.png")
            cardRegion = (cardWidthStart, suitHeightTop, cardWidthEnd, suitHeightBottom)
            cardIm = im.crop(cardRegion)
            cardRegionSize = cardIm.size
            for i in cardRegionSize:
                tupleSet.append(round(0.8 * i))
            cardRegionSize = tuple((tupleSet[0],tupleSet[1]))
            self.image = cardIm.resize(cardRegionSize)

        def getImage(self):
            return self.image
        
    for i in Suits:
        for j in Cards:
            name = j+i
            if j.isnumeric():
                modif = 0
                value = j
            elif j == "T":
                value = 10
            elif j == "J":
                value = 11
            elif j == "Q":
                value = 12
            elif j == "K":
                value = 13
            elif j == "A":
                modif = 13
                value = 1
            else:raise TypeError("Code not right")
            Deck.append(Card(value, name, modif))
    print("Initialize complete")
    return Deck
