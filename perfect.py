from card_game import Cards

##some horrible code written in 20mins to find score with theoretical perfect play

#chopped this out of the player class, dont really want to create player just for this
def f_cumulative_score(lis,d):
    for i in range(0,len(lis)):
        #lis[i][0] += self.score 
        for j in range(1,d):
            lis[i][j] += lis[i][j-1]
    return lis

exp = 5
n=pow(10,exp)
res =[]
for i in range(0,n):
    #create n sets of shuffled decks
    deck = Cards()
    deck.shuffle()
    v = [deck.cards[key] for key in deck.order]
    res.append(v)

#find score progression throughout game
c_score = f_cumulative_score(res,len(deck.order))

#find the best acheivable score with perfect play and full knowledge of cards
best=[]
for i in range(0,n):
    j=0
    while c_score[i][j]<26 and j<len(deck.order)-1:
        j+=1
    best.append(max(c_score[i][0:j]))

#turn score to points
points=[]
for i in range(0,len(best)):
    if best[i]>15 and best[i]<26:
        points.append(25-best[i])
    else:
        points.append(10)
points_ave = sum(points)/len(points)

#print(points)
print(points_ave)