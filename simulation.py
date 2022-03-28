#Simulation
import math
import random

# 'w' for wong_halves ---- level 3
# 'z' for zen_count ---- level 2
# 'h' for hi_lo ---- level 1
style = 'z'

counting_style = {'w': {.5:{'2','7'}, 1:{'3','4','6'}, 1.5:{'5'}, -.5:{'9'}, -1:{'10', 'J', 'Q', 'K', 'A'}, 0:{'8'}}, 
				  'z': {1:{'2','3','7'}, -1:{'A'}, 2:{'4','5','6'}, -2:{'10', 'J', 'Q', 'K'}, 0:{'8','9'}}, 
				  'h': {1:{'2','3','4','5','6'}, 0:{'7','8','9'}, -1:{'A', '10', '9', '8', 'J', 'Q', 'K'}}
				 }

cardToNum = {'A': 1,'J': 10, 'Q': 10, 'K': 10, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10}

NUM_ITER = 100
NUM_DECKS = 6

card_count = 0
deck_pool = [str(i) for _ in range(NUM_DECKS) for i in {'A', 'Q', 'K', 'J', *range(2,11)}]

#Reset deck at every half (Playing with a shoe that shuffles at 50%)
def reset_deck():
  deck_pool = [str(i) for _ in range(NUM_DECKS) for i in {'A', 'Q', 'K', 'J', *range(2,11)}]

def drawCard():
  ind = random(0, len(deck_pool)-1)
  card = deck_pool[ind]
  deck_pool = deck_pool[:ind]+deck_pool[ind+1:]
  for point_val in counting_style[style]:
    if card in counting_style[style][poing_val]:
      card_count += point_val
      break
  return cardToNum[card]

win = 0
loss = 0
for _ in len(NUM_ITER):
  dealer = 0
  player = 0

  #initial hand
  player += drawCard()
  player += drawCard()

  

  if len(deck_pool) <= NUM_DECKS*13:
    reset_deck()
  
  
