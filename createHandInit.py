### ----- initializing the deck ----- ###
def Initialize():
    Cards = ["2","3","4","5","6","7","8","9","T","J","Q","K","A"]
    Suits = ["h","c","d","s"]
    fullHand = []

    print("Initialize running")
    class Card:
        value = 0
        name = ""
        modif = 0
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

    while len(fullHand) != 7:
        j = input("Name of Card: ")
        
        name = j
        modif = 0
        
        if j[0].isnumeric():
            value = int(j[0])
        elif j[0] == "T":
            value = 10
        elif j[0] == "J":
            value = 11
        elif j[0] == "Q":
            value = 12
        elif j[0] == "K":
            value = 13
        elif j[0] == "A":
            modif = 13
            value = 1
        fullHand.append(Card(value, name, modif))
    print("Hand Created")
    return fullHand
        
