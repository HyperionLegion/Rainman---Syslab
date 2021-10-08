import random
#example 5s: 5 of spades
#S = spades, H = hearts, C = clubs, D = diamonds
cards = {"2s": 1, "3s": 1,"4s": 1,"5s": 1,"6s": 1,"7s": 1,"8s": 1,"9s": 1,"10s": 1,"Js": 1,"Qs": 1,"Ks": 1,"As": 1,
"2h": 1, "3h": 1,"4h": 1,"5h": 1,"6h": 1,"7h": 1,"8h": 1,"9h": 1,"10h": 1,"Jh": 1,"Qh": 1,"Kh": 1,"Ah": 1,
"2d": 1, "3d": 1,"4d": 1,"5d": 1,"6d": 1,"7d": 1,"8d": 1,"9d": 1,"10d": 1,"Jd": 1,"Qd": 1,"Kd": 1,"Ad": 1,
"2c": 1, "3c": 1,"4c": 1,"5c": 1,"6c": 1,"7c": 1,"8c": 1,"9c": 1,"10c": 1,"Jc": 1,"Qc": 1,"Kc": 1,"Ac": 1,}
count = 0 #usually stand if true count > 4 otherwise hit

def upCount():
    count += 1

def downCount():
    count -=1

def isLeft(s):
    return cards[s]

def remove(s):
    cards[s] = cards[s]-1

def addDeck(num):
    for i in cards.keys():
        cards[i] += num

def reshuffle(num):
    for i in cards.keys():
        cards[i] = num

def getValue(i, curr=0):
    suit = i[0:-1]
    if suit =='A':
        if(curr < 11):
            return 11
        else:
            return 1
    else:
        if suit == 'J' or suit =='K' or suit=='Q':
            suit = '10'
        return int(suit)

def possibleScores(curr):
    scores = {}
    for i in range(1,12):
        scores[i] = 0
    for i in cards.keys():
        if isLeft(i):
            suit = i[0:-1]
            if suit =='A':
                if(curr < 11):
                    scores[int('11')] += cards[i]
                scores[int('1')] += cards[i]
            else:
                if suit == 'J' or suit =='K' or suit=='Q':
                    suit = '10'
                scores[int(suit)] += cards[i]
    return scores

def probBust(i):
    total = 0
    scores = possibleScores(i)
    for j in range(1,12):
        total += scores[j]
    over = 0
    maxUnder = 21-i
    for j in range(maxUnder+1,12):
        over += scores[j]
    #print(total)
    #print(over)
    return float(over/total)

def sim():
    runs = 0
    money = 1000
    count = 0
    addDeck(4)
    while runs < 40:
        possible = []
        for i in cards.keys():
            if cards[i] > 0:
                possible.append(i)

        #initial hand
        hand = 0
        rand = random.randrange(len(possible))
        remove(possible[rand])
        hand += getValue(possible[rand], hand)
        if getValue(possible[rand], hand) > 9:
            count = count - 1
        elif getValue(possible[rand], hand)<7:
            count = count + 1

        for i in cards.keys():
            if cards[i] > 0:
                possible.append(i)
        rand = random.randrange(len(possible))
        remove(possible[rand])
        hand += getValue(possible[rand], hand)
        if getValue(possible[rand], hand) > 9:
            count = count - 1
        elif getValue(possible[rand], hand)<7:
            count = count + 1

        #hit if count > 4
        if count/5 < 4 or hand < 17:
        #if random.random() > 0.5:
            for i in cards.keys():
                if cards[i] > 0:
                    possible.append(i)
            rand = random.randrange(len(possible))
            remove(possible[rand])
            hand += getValue(possible[rand])
            if getValue(possible[rand], hand) > 9:
                count = count - 1
            elif getValue(possible[rand], hand)<7:
                count = count + 1


        #dealer draws
        dealer = 0
        while dealer < 17:
            for i in cards.keys():
                if cards[i] > 0:
                    possible.append(i)
            rand = random.randrange(len(possible))
            remove(possible[rand])
            dealer += getValue(possible[rand])
            if getValue(possible[rand], hand) > 9:
                count = count - 1
            elif getValue(possible[rand], hand)<7:
                count = count + 1
                

        #score
        if hand > 21:
            money = money - 50
            #print('loss')
        if hand == 21:
            money = money + 150
            #print('win')
        elif dealer > 21:
            money = money + 50
            #print('win')
        else:
            if dealer <= 21 and hand < 21:
                if dealer > hand:
                    money = money - 50
                   # print('loss')
                elif hand > dealer:
                    money = money + 50
                    #print('win')
        print(hand, dealer)
        print(money)
        runs += 1
    return money

wins = 0
loss = 0
for i in range(0, 100):
    reshuffle(4)
    if sim() > 1000:
        wins += 1
    elif sim() < 1000:
        loss += 1
print(wins)
print(loss)
#sim()
