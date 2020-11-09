import random

class Game():

    def start(self):
        self.c = Cards()
        self.c.shuffle()
        self.player = SimplePlayer()
        self.finished = False

    def play(self):
        while not self.finished:
            self.step()

    def step(self):
        #check if cards left before draw
        if self.c.cards_left == False:
            self.end_game(self.player)
        else:
            d = self.player.play(self.c)
            if d == 'stick':
                self.end_game(self.player)
            
        #check if bust after draw
        if self.player.score>25:
            print('bust')
            self.end_game(self.player)

    def end_game(self,player):
        if player.score >25 or player.score <16:
            points = 10
        else:
            points = 25-player.score
        self.finished = True
        #print(self.cards_remaining)
        print('cards: '+str(player.cards_dealt))
        print("score: "+str(player.score))
        print('points :'+str(points))


class Cards():
    def __init__(self):
        #list of cards in game
        self.cards = {
            "rA":-1,
            "r2":-2,
            "r3":-3,
            "r4":-4,
            "r5":-5,
            "r6":-6,
            "r7":-7,            
            "r8":-8,
            "r9":-9,
            "r10":-10,
            "rJ":-10,
            "rQ":-10,
            "rK":-10,

            "b2":2,
            "b3":3,
            "b4":4,
            "b5":5,
            "b6":6,
            "b7":7,            
            "b8":8,
            "b9":9,
            "b10":10,
            "bJ":10,
            "bQ":10,
            "bK":10,
            "bA":11,
        }

        self.shuffledcards = {}
        self.order = list(self.cards.keys())
        self.n = 0
        self.cards_left = True

    def shuffle(self):
        random.shuffle(self.order)    
        for key in self.order:
            self.shuffledcards[key] = self.cards[key]
        self.cards = self.shuffledcards

    def deal(self):
        #deal card, returns name and nominal value
        if self.n+1==len(self.order):
            self.cards_left = False
        card = self.order[self.n]
        value = self.cards[self.order[self.n]]
        self.n += 1
        return card,value

class SimplePlayer():
    def __init__(self):
        self.cards_remaining = {
            "rA":-1,
            "r2":-2,
            "r3":-3,
            "r4":-4,
            "r5":-5,
            "r6":-6,
            "r7":-7,            
            "r8":-8,
            "r9":-9,
            "r10":-10,
            "rJ":-10,
            "rQ":-10,
            "rK":-10,

            "b2":2,
            "b3":3,
            "b4":4,
            "b5":5,
            "b6":6,
            "b7":7,            
            "b8":8,
            "b9":9,
            "b10":10,
            "bJ":10,
            "bQ":10,
            "bK":10,
            "bA":11,
        }

        self.cards_dealt ={}
        self.score = 0

    def play(self,deck):
        if self.score>17:
            return 'stick'
        else:
            self.draw_card(deck)
            return 'draw'

    def draw_card(self,deck):
        card,value = deck.deal()
        self.cards_remaining.pop(card)
        self.cards_dealt[card] = value
        self.score+=value


