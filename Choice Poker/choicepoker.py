#CHOICE POKER
import random
import json
import math
import time

def get_settings():
    file = open("settings.json")
    data = json.load(file)
    file.close()
    carddata = list(zip(data["cardnames"], data["cardvalues"]))
    cards = {}
    for card in carddata:
        name = card[0]
        cards[name] = card[1]        
    return data["startingbalance"], cards, data["raisechance"], data["participationfee"]

startbalance,cards,raisechance,fee = get_settings()

balance = startbalance
cpubalance = startbalance

hand = [None, None, None, None, None]
cpuhand = [None, None, None, None, None]

def reset_stats():
    global startbalance
    global balance
    global cpubalance
    global hand
    global cpuhand
    balance = startbalance
    cpubalance = startbalance

    hand = [None, None, None, None, None]
    cpuhand = [None, None, None, None, None]

running = True

def place_bet(prompt, balance):
    error = True
    while error:
        try:
            bet = int(input(prompt))
            if bet <= balance:
                error = False
            else:
                print("Dealer: You cannot bet more chips than you have...")
        except ValueError:
            print("Dealer: Please enter a number...")
    return bet

def deal_card(x):
    name = list(cards.keys())
    return cards[random.choice(name)]

def print_hand(hand, player=True):
    rs = None
    if player:
        rs = "Your hand: "
    else:
        rs = "CPU hand: "
    value = sum(hand)
    for i in range(len(hand)):
        currentcard = hand[i]
        names = list(cards.keys())
        rs += "%s " % (names[currentcard-1].title())
    print(rs)
    if player:
        print("Your value: %s" % (value))
    else:
        print("CPU value: %s" % (value))

def handle_raise(prompt):
    error = True
    while error:
        ret = None
        choice = input(prompt)
        if choice.lower() == 'y':
            ret = True
            error = False
        elif choice.lower() == 'n':
            ret = False
            error = False
        else:
            print("Dealer: Please type in Y (Yes) or N (No)")
    return ret

def start_game():
    global balance
    global cpubalance
    global hand
    global cpuhand
    if fee != 1:
        print("Dealer: The participation fee is %s chips." % (fee))
    else:
        print("Dealer: The participation fee is %s chip." % (fee))
    balance -= fee
    print("Dealer: Time to deal your hands!")
    hand = list(map(deal_card, hand))
    cpuhand = list(map(deal_card, cpuhand))
    print_hand(hand)
    print("Dealer: Place your bets.")
    bet = place_bet("", balance)
    balance -= bet
    cpubet = random.randint(1, math.ceil(cpubalance/5))
    cpubalance -= cpubet
    print("Dealer: Thank you, we can now procede to the raising phase.")
    raising = True
    playercontinue = None
    cpucontinue = True
    while raising:
        rise = 0
        cpurise = 0
        print(playercontinue, cpucontinue)
        prompt = "Dealer: Your bet is currently %s chips, Your opponent\'s bet is currently %s chips. Would you like to raise? (Y/N)" % (bet, cpubet)
        playercontinue = handle_raise(prompt)
        if playercontinue:
            rise = place_bet("Dealer: Please enter the amount of chips you want to raise by.", balance)
            bet += rise
        if cpucontinue:
            ran = random.randint(1, 100)
            if ran <= raisechance:
                cpucontinue = True
                cap = math.ceil(cpubalance/2)
                cpuraise = random.randint(1, cap)
                cpubalance -= cpuraise
                cpubet += cpuraise
            else:
                cpucontinue = False
        if playercontinue == False and cpucontinue == False:
            raising = False
    choice = None
    if bet >= cpubet:
        print("Dealer: The player has the choice...")
        choice = handle_raise("Dealer: Would you want to go higher (Y) or lower (N)")
    elif cpubet < bet:
        if cpubet < 13*5/2:
            choice = False
        else:
            choice = True
    print("Dealer: Now all the raises are done. Now we can procede to showdown!")
    print("Dealer: In...")
    for i in range(3):
        print("Dealer: %s" % (3-i))
        time.sleep(1)
    print("Dealer: SHOWDOWN!")
    print_hand(hand)
    print_hand(cpuhand, False)
    if choice:
        if sum(hand) >= sum(cpuhand):
            print("Dealer: The player is the winner!")
        else:
            print("Dealer: The opponent is the winner!")
    else:
        if sum(hand) <= sum(cpuhand):
            print("Dealer: The player is the winner")
        else:
            print("Dealer: The opponent is the winner!")
        
    

    
while running:
    choice = handle_raise("Dealer: Do you want to play Y/N?")
    if choice:
        start_game()
        reset_stats()
    else:
        print("Dealer: Leaving the game!")
        break
