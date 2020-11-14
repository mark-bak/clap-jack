##Some code to simulate an odd card game with different play strategies
import random
import math
from itertools import permutations
import matplotlib.pyplot as plt

class Game():
    ## Requires player as argument (inherit from SimplePlayer)
    ## Handles each turn, ending of game
    ## Game.start() resets game and player, Game.play() plays until bust, no cards or player sticks and returns points won
    def __init__(self,player):
        self.player = player
        self.c = Cards()

    def start(self):
        #self.c = Cards()
        self.c.reset()
        self.c.shuffle()
        self.player.reset()
        self.finished = False

    def play(self):
        while not self.finished:
            p = self.step()
        return p

    def step(self):
        #this logic could maybe be made simpler but it works       
        #check if cards remaining or player is bust
        if self.c.cards_left == False or self.player.score>25:
            p = self.end_game(self.player)
        else:
            #see what player wants to do, stick or get new card dealt
            decision = self.player.decide()
            if decision == 'stick':
                p = self.end_game(self.player)
            else:
                card,value = self.c.deal()
                self.player.update(card,value)
        if self.finished == True:
            #return points at end of game
            return p 

    def end_game(self,player):
        if player.score >25 or player.score <16:
            points = 10
        else:
            points = 25-player.score
        self.finished = True
        return points


class Cards():
    ## Deck of cards used in game, with shuffle() and deal() methods
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
        self.order = list(self.cards.keys())
        self.n = 0
        self.cards_left = True

    def reset(self):
        self.n=0
        self.order = list(self.cards.keys())
        self.cards_left = True

    def shuffle(self):
        random.shuffle(self.order)    

    def deal(self):
        #deals next card, returns name and nominal value
        if self.n+1==len(self.order): # check cards left
            self.cards_left = False
        card = self.order[self.n]
        value = self.cards[self.order[self.n]]
        self.n += 1
        return card,value

class SimplePlayer():
    ## Player that has reset, update methods req for Game(). To make own player inherit from this and
    ## override decide() method
    def __init__(self):
        #used to be something here
        pass
    
    def reset(self):
        self.deck=Cards()
        self.cards_dealt ={}
        self.score = 0
        self.cards_remaining = self.deck.cards

    def decide(self):
        #always draw and therefore always lose
        return 'draw'

    def update(self,card,value):
        self.cards_remaining.pop(card)
        self.cards_dealt[card] = value
        self.score+=value

    def cumulative_score(self,lis,d,cur_score):
        for i in range(0,len(lis)):
            lis[i][0] += cur_score #add current score to first item
            for j in range(1,d):
                lis[i][j] += lis[i][j-1] #get cumulative score
        return lis

class StickPlayer(SimplePlayer):
    ##Improved player that sticks on turn if score>val
    def __init__(self,stick_val):
        super().__init__()
        self.stick_val = stick_val

    def decide(self):
        if self.score>=self.stick_val:
            return 'stick'
        else:
            return 'draw'

class ImpStickPlayer(SimplePlayer):
    ##Improved player that sticks on turn if score>val and also will change +11 ace to +1 if it will make bust
    def __init__(self,stick_val):
        super().__init__()
        self.stick_val = stick_val

    def decide(self):
        if self.score>=self.stick_val:
            return 'stick'
        else:
            return 'draw'

    def update(self,card,value):
        #set black ace from +11 to +1 if it makes you bust
        if card == 'bA' and self.score+value>25:
            value = 1
        self.cards_remaining.pop(card)
        self.cards_dealt[card] = value
        self.score+=value

class ProbPlayer(SimplePlayer):
    ## Player that when it is in lategame (cards_rem<depth) and is in scoring position, searches to see if the expected points from
    ## playing on are better than current and uses this to decide wether to draw
    def __init__(self,stick_val,depth):
        super().__init__()
        self.stick_val = stick_val
        self.depth=depth

    def decide(self):
        n_rem_cards = len(self.cards_remaining)

        if self.score>15 and n_rem_cards<=self.depth:
            #this happens when in scoring position and in lategame
            perms = list(permutations(self.cards_remaining.values(),n_rem_cards))
            permslist = [list(t) for t in perms]
            cumulative_score = self.cumulative_score(permslist,n_rem_cards,self.score)
            p_ex = self.determine_prob(cumulative_score,n_rem_cards) # expected score
            if p_ex>25-self.score:
                #if expected points are higher (worse) stick
                return 'stick'

        if self.score>=self.stick_val and n_rem_cards>self.depth:
            #if not in lategame, stick on values score>val
            return 'stick'
        else:
            #otherwise draw
            return 'draw'

    def determine_prob(self,c_s,d):
        ##there is a small problem with how this evaluates winning positions (just takes a score as winning) - can be fixed with
        ## recursively applying this method in scoring permutations, but this gets slow and messy :(
        points =[]
        #set of lists for which permutations stil need to be checked (i.e have not been determined bust or winning)
        check_ind = []
        check_ind_next = list(range(0,len(c_s)))

        for j in range(0,d):
            #copy values to check for next iteration
            check_ind = check_ind_next[:]
            check_ind_next.clear()
            
            #check whether lines are bust or winning
            for i in check_ind:
                if c_s[i][j]>25:  
                    #bust                
                    points.append(10)
                elif c_s[i][j]>15 and c_s[i][j]<=25:
                    #c_new = [v[j+1:d] for v in c_s]
                    #scores.append(self.determine_prob(c_new,d-(j+1))) # some funky recursion, can gt rid as is slows down a lot for not much improve
                    points.append(25-c_s[i][j]) # slightly underestsimates expected score, but so much quicker than doing the recursion
                else:
                    #add non bust or winning permutations to next iteration for checking
                    check_ind_next.append(i)
                    
        points = points+[10]*len(check_ind) #all remaining perms not already checked will be worth 10 (out of cards)

        # a really roundabout way to just get the mean, but its staying for now :) as this is how I thought it through
        if len(c_s)==0:
            base_prob = 0
        else:
            base_prob = 1/len(c_s)
        points_exp = sum(points)*base_prob

        return points_exp

class ImpProbPlayer(ProbPlayer):
    ## Same as prob player but goes bust less as it changes the bA+11 to -1 when immediately about to go bust
    ## This one is decent improvement on just sticking - still reckon theres a lot of improvement possible with different
    ## stick values at different earlier game stages, and more accurate and efficient calculator of effective score lategame
    def __init__(self,stick_val,depth):
        super().__init__(stick_val,depth)

    def update(self,card,value):
        #set ace low if it makes you bust
        if card == 'bA' and self.score+value>25:
            value = 1
        self.cards_remaining.pop(card)
        self.cards_dealt[card] = value
        self.score+=value
    

def play_games(player,no_games):
    ## test function to play lots of games with a certain player and return points scored as a list
    game = Game(player)
    points = []
    for i in range(0,no_games):
        game.start()
        points.append(game.play())
    return points


if __name__ == "__main__":
    #stops these tests from running if this is imported as a module
    
    exp = 5 #run 10^exp games
    n_g = pow(10,exp)
    ## find optimal stick value ##
    vals = [16,17,18,19,20,21,22,23,24,25]
    valstr = [str(v) for v in vals]
    res=[]
    for v in vals:
        player = StickPlayer(v)
        res.append(play_games(player,n_g))
    res_ave =[sum(r)/len(r) for r in res]

    #plotting
    plt.figure(1)
    plt.bar(valstr,res_ave)
    for i,v in enumerate(res_ave):
        plt.text(i-.3,v+.1,str(round(v,2)))
    plt.ylim([0,10])
    plt.title('bA = 11, rA = -1')
    plt.xlabel('Stick number')
    plt.ylabel('Mean points after $10^{}$ games'.format(str(exp)))

    ## compare optimal stick, improved aces and prob player ##
    res2 = []
    player = StickPlayer(19)
    res2.append(play_games(player,n_g))
    player = ImpStickPlayer(19)
    res2.append(play_games(player,n_g))
    player = ProbPlayer(19,7)
    res2.append(play_games(player,n_g))
    player = ImpProbPlayer(19,7)
    res2.append(play_games(player,n_g))

    res2_ave =[sum(r)/len(r) for r in res2]

    labels=['S_19','S_19_Ace','S_19_P','S_19_P_Ace']
    #plotting
    plt.figure(2)
    plt.bar(labels,res2_ave)
    for i,v in enumerate(res2_ave):
        plt.text(i-.1,v+.1,str(round(v,2)))
    plt.ylim([0,10])
    plt.title('Comparison of improved strategies')
    plt.xlabel('Strategy')
    plt.ylabel('Mean points after $10^{}$ games'.format(str(exp)))

    #show the beautiful plots
    plt.show()