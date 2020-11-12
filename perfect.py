from card_game import Cards
from card_game import SimplePlayer as SP
from collections import Counter

##some absolutely horrible code written in 60mins to find score with theoretical perfect play

def create_n_shuffled_decks(n):
    #create n sets of shuffled decks
    ret =[]
    for i in range(0,n):
        deck = Cards()
        deck.shuffle()
        v = [deck.cards[key] for key in deck.order]
        ret.append(v)
    length = len(deck.order)
    return ret,length

def find_ideal_score(c_score):
    #finds the ideal score possible with full knowledge of card order
    best=[]
    length = len(c_score[0])
    for i in range(0,len(c_score)):
        j=0
        while c_score[i][j]<26 and j<length-1:
            j+=1
        best.append(max(c_score[i][0:j]))
    return best

def find_points(ideal_scores):
    #converts game scores into points
    points=[]
    for i in range(0,len(ideal_scores)):
        if ideal_scores[i]>15 and ideal_scores[i]<26:
            points.append(25-ideal_scores[i])
        else:
            points.append(10)
    points_ave = sum(points)/len(points)
    return points,points_ave

def get_ace_combos(shuf_d):
    ## this is horrible
    bAp11_rAn11 = [x[:] for x in shuf_d]
    bAp1_rAn1 = [x[:] for x in shuf_d]
    bAp1_rAn11 = [x[:] for x in shuf_d]
    for i in range(0,len(bAp11_rAn11)):
        ind = bAp11_rAn11[i].index(-1)
        bAp11_rAn11[i][ind] = -11
    for i in range(0,len(bAp1_rAn1)):
        ind = bAp1_rAn1[i].index(11)
        bAp1_rAn1[i][ind] = 1
    for i in range(0,len(bAp1_rAn11)):
        ind = bAp1_rAn11[i].index(11)
        bAp1_rAn11[i][ind] = 1
        ind = bAp1_rAn11[i].index(-1)
        bAp1_rAn11[i][ind] = -11
    return shuf_d,bAp11_rAn11,bAp1_rAn1,bAp1_rAn11

def find_best_game(ideals):
    best_possible_score = []
    pos=[]
    for i in range(0,len(ideals[0])):
        #this really shouldnt be harcoded like this but oh well
        l = [ideals[0][i],ideals[1][i],ideals[2][i],ideals[3][i]]
        best_possible_score.append(max(l))
        pos.append(l.index(best_possible_score[-1]))
    return best_possible_score,pos

#tests 
if __name__=='__main__':
    exp = 5
    n=pow(10,exp)

    shuf_d,length = create_n_shuffled_decks(n)
    shuf_d,b11_r11,b1_r1,b1_r11 = get_ace_combos(shuf_d)
    acegames = [shuf_d,b11_r11,b1_r1,b1_r11]
    ideal =[]
    for games in acegames:
        c_score = SP.cumulative_score(None,games,length,0) #find score progression throughout game - not sure this is the best wat to use this method with the None??
        ideal.append(find_ideal_score(c_score))
    scores,pos = find_best_game(ideal)
    p,p_ave = find_points(scores)
    
    freq = Counter(pos)
    freq_list=[]
    for i in range(0,len(freq)):
        freq_list.append(round(100*freq[i]/n))
    
    print(p_ave)
    print(freq_list)