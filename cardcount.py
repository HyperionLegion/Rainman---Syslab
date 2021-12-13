import random
#example 5s: 5 of spades
#S = spades, H = hearts, C = clubs, D = diamonds
cards = {"2s": 1, "3s": 1,"4s": 1,"5s": 1,"6s": 1,"7s": 1,"8s": 1,"9s": 1,"10s": 1,"Js": 1,"Qs": 1,"Ks": 1,"As": 1,
"2h": 1, "3h": 1,"4h": 1,"5h": 1,"6h": 1,"7h": 1,"8h": 1,"9h": 1,"10h": 1,"Jh": 1,"Qh": 1,"Kh": 1,"Ah": 1,
"2d": 1, "3d": 1,"4d": 1,"5d": 1,"6d": 1,"7d": 1,"8d": 1,"9d": 1,"10d": 1,"Jd": 1,"Qd": 1,"Kd": 1,"Ad": 1,
"2c": 1, "3c": 1,"4c": 1,"5c": 1,"6c": 1,"7c": 1,"8c": 1,"9c": 1,"10c": 1,"Jc": 1,"Qc": 1,"Kc": 1,"Ac": 1,}
decks = 2
count = 0
cards_played = 0

def isLeft(s):
    return cards[s]

def remove(s):
    cards[s] = cards[s]-1

def resetDeck(num):
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

def drawCard(curr):
    global count
    global cards_played
    possible = []
    for i in cards.keys():
        if cards[i] > 0:
            for j in range(cards[i]):
                possible.append(i)
    rand = random.randrange(len(possible))
    remove(possible[rand])
    cards_played += 1
    #card count
    if possible[rand][0:-1] == 'A':
        count-=1
    elif getValue(possible[rand], curr) > 9:
        count -= 1
    elif getValue(possible[rand], curr)<7:
        count += 1
    return getValue(possible[rand], curr)


def sim():
    runs = 0
    money = 2500
    global count
    global decks_left
    global cards_played
    decks_left = decks
    cards_played = 0
    count=0
    betSize = 5
    resetDeck(decks)
    while runs < 10:
        decks_left = decks - (cards_played//52)
        #initial hand
        hand = 0
        hand += drawCard(hand)

        #2nd card
        hand += drawCard(hand)

        #dealer draws
        dealer = 0
        dealer += drawCard(dealer)

        # while hand <12:
        # if (hand==-11 and dealer==11) or (hand==10 and (dealer==10 or dealer==11)) or (hand==9 and (dealer==2 or (dealer<=11 and dealer>=7))) or (hand<=8) or (hand==12 and dealer!=4 and dealer!=5 and dealer!=6) or (hand>=13 and hand<=16 and (dealer<2 or dealer>6)):
            # hand +=drawCard(hand)

        while dealer < 17:
            dealer += drawCard(dealer)

        if count/decks_left > 0:
            if hand < 16:
                hand += drawCard(hand)
        
        elif count/decks_left < 0:
            if hand <= 16:
                hand += drawCard(hand)
            # elif dealer < 10:
            #     hand += drawCard(hand)
        else:
            if hand < 17:
                hand += drawCard(hand)
        
        #bet high if there is a high true count
        #1-8 bet spread
        if count/decks_left >= 3:
        #if random.random() > 0.5:
            # hand += drawCard(hand)
            betSize = 80
        elif count/decks_left >=2:
            betSize = 40
        elif count/decks_left >=1:
            betSize = 20
        else:
            betSize=10

        # if count/decks_left < 2:
        #     betSize = 10
        # else:
        #     betSize = 25*(count/decks_left-1)

        #score
        if hand > 21:
            money = money - betSize
            #print('loss')
        elif hand == 21 and dealer != 21:
            money = money + betSize*1.5
            #print('win')
        elif dealer > 21:
            money = money + betSize
            #print('win')
        else:
            if dealer <= 21 and hand < 21:
                if dealer > hand:
                    money = money - betSize
                   # print('loss')
                elif hand > dealer:
                    money = money + betSize
                    #print('win')
        #print(hand, dealer)
        # print(money)
        runs += 1
    return money


wins = 0
loss = 0
for i in range(0, 100):
    score = sim()
    if score >= 2500:
        wins += 1
    else:
        loss += 1
# print(sim())
print(wins)
print(loss)
    