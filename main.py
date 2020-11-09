import random
from itertools import permutations

class Game():

    def __init__(self,player):
        self.player = player

    def start(self):
        self.player.reset()
        self.c = Cards()
        self.c.shuffle()
        self.finished = False

    def play(self):
        while not self.finished:
            p = self.step()
        return p

    def step(self):
        
        #check if cards remaining or player is bust
        if self.c.cards_left == False or self.player.score>25:
            p = self.end_game(self.player)
        else:
            #see what palyer wants to do, stick or get new card dealt
            decision = self.player.decide()
            if decision == 'stick':
                p = self.end_game(self.player)
            else:
                card,value = self.c.deal()
                self.player.update(card,value)
        if self.finished == True:
            return p 

    def end_game(self,player):
        if player.score >25 or player.score <16:
            points = 10
        else:
            points = 25-player.score
        self.finished = True
        #print(self.cards_remaining)
        #print('cards: '+str(player.cards_dealt))
        #print("score: "+str(player.score))
        #print('points :'+str(points))
        return points


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
        if self.n+1==len(self.order): # check cards left
            self.cards_left = False
        card = self.order[self.n]
        value = self.cards[self.order[self.n]]
        self.n += 1
        return card,value

class SimplePlayer():
    #def __init__(self,stick_val):
        #self.stick_val = stick_val
    
    def reset(self):
        self.cards_dealt ={}
        self.score = 0
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

    def decide(self):
        #if self.score>self.stick_val:
        #    return 'stick'
        #else:
        return 'draw'

    def update(self,card,value):
        self.cards_remaining.pop(card)
        self.cards_dealt[card] = value
        self.score+=value

class StickPlayer(SimplePlayer):
    def __init__(self,stick_val):
        self.stick_val = stick_val

    def decide(self):
        if self.score>self.stick_val:
            return 'stick'
        else:
            return 'draw'

class ProbPlayer(SimplePlayer):
    def __init__(self,depth):
        self.depth = depth

    def decide(self):
        if self.score>15:
            value_list = self.cards_remaining.values()
            perms = permutations(value_list,self.depth)
            search = ProbSearch(list(perms),self.depth,self.score)
            search.prune()
            r = search.tot_score()
            print('score:'+str(self.score))
            print('winning'+str(search.winners))
            print('losing'+str(search.losers))

            #print(list(perms))
            
            return 'stick'
        else:
            return 'draw'


class ProbSearch():
    def __init__(self,perms,depth,score):
        self.winners = perms
        for i in range(0,len(self.winners)):
            self.winners[i] = list(self.winners[i])
        self.losers = []
        self.cum_score =[]
        self.depth = depth
        self.score = score

    def prune(self):
        while self.score + self.winners[-1][0]>25:
            ret = self.winners.pop(-1)
            self.losers.append(ret)

    def tot_score(self):
        self.cum_score = [self.score]*len(self.winners)
        for i in range(1,self.depth):
            self.cum_score = [self.cum_score, list(self.winners[:][i-1])] 
            print(self.cum_score)






res=[]
vals = [18]

for v in vals:
    p=[]
    player = StickPlayer(v)
    game = Game(player)
    for i in range(0,10000):
        game.start()
        p.append(game.play())
    res.append(round(sum(p)/len(p),2))

depth = [2]
for q in depth:
    player = ProbPlayer(q)
    game = Game(player)
    p=[]
    for i in range(0,1):
        game.start()
        p.append(game.play())
    res.append(round(sum(p)/len(p),2))

print(res)

    