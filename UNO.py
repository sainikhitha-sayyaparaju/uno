import random
import time
from colorama import Fore
def build_deck():
    deck = []
    colors = ["red", "green", "blue", "yellow"]
    values = [0,1,2,3,4,5,6,7,8,9, "drawtwo", "skip", "reverse"]
    wilds = ["wild drawfour", "wild"]
    for color in colors:
        for value in values:
            deck.append("{} {}".format(color, value))
    for _ in range(4):
        deck.append(wilds[0])
        deck.append(wilds[1])
    return deck
def cards_drawn(num):
    cards = []
    for i in range(num):
        cards.append(unoDeck.pop(0))
    return cards


def shuffle_deck(deck):
    length = len(deck)
    for i in range(length):
        n = random.randint(0, length - 1)
        deck[i], deck[n] = deck[n], deck[i]
    return deck




def show_hand(player, playerHand, names):
    print(Fore.WHITE+"Player {}".format(names[player]))
    print(Fore.WHITE+"Your Hand")
    print(Fore.WHITE+"----------------")
    y = 1
    for card in playerHand:
        color = card.split()[0].upper()
        if color == "wild":
            print(Fore.WHITE+"{}) {}".format(y, card))
        elif color == "RED":
            print(Fore.RED + "{}) {}".format(y, card))
        elif color == "BLUE":
            print(Fore.BLUE + "{}) {}".format(y, card))
        elif color == "GREEN":
            print(Fore.GREEN + "{}) {}".format(y, card))
        elif color == "YELLOW":
            print(Fore.YELLOW + "{}) {}".format(y, card))
        else:
            print(Fore.WHITE + "{}) {}".format(y, card))
        y += 1
    print("")


def can_play(color, value, playerHand):
    for card in playerHand:
        if "wild" in card:
            return True
        elif color in card or value in card:
            return True
    return False


def can_add_card(value, playerHand):
    for card in playerHand:
        if value in card:
            return True
    return False

def player_increment():
    global playerDirection, playerTurn
    playerTurn += playerDirection
    if playerTurn == num:
        playerTurn = 0
    elif playerTurn < 0:
        playerTurn = num - 1

def reverse():
    global playerDirection
    playerDirection *= -1

def skip():
    global playerDirection, playerTurn
    player_increment()

def draw(n):
    global playerDirection, playerTurn, players, playerDraw
    playerDraw = playerTurn + playerDirection
    if playerDraw == num:
        playerDraw = 0
    elif playerDraw < 0:
        playerDraw = num - 1
    players[playerDraw].extend(cards_drawn(n))

def wild():
    global currentColor, colors
    print(Fore.RED + "1) red")
    print(Fore.GREEN + "2) green")
    print(Fore.BLUE + "3) blue")
    print(Fore.YELLOW + "4) yellow")
    print(Fore.WHITE + "what color would you like to chose? -->")
    chosenColor = int(input())
    while chosenColor < 1 or chosenColor > 4:
        chosenColor = int(input(Fore.WHITE + "invalid color. Enter a valid color? -->"))
    currentColor = colors[chosenColor - 1]

while True:
    names = {}
    print(Fore.WHITE + "Welcome to the game!!!!!")
    print(Fore.WHITE + "-----------------------")
    print(Fore.WHITE + "finish your cards first to win")
    unoDeck = build_deck()
    unoDeck = shuffle_deck(unoDeck)
    unoDeck = shuffle_deck(unoDeck)
    discards = []
    num = int(input(Fore.WHITE + "enter number of players? -->"))
    while num < 2 or num > 4:
        print(Fore.WHITE + "not possible")
        num = int(input(Fore.WHITE + "enter number of players? -->"))
    for i in range(num):
        names[i] = input(Fore.WHITE + "enter player {} name".format(i + 1))
    cards_num = int(input(Fore.WHITE + "enter number of cards? -->"))
    players = []
    for i in range(num):
        players.append(cards_drawn(cards_num))
    playerTurn = 0
    playerDirection = 1
    playing = True
    colors = ["red", "green", "blue", "yellow"]
    discards.append(unoDeck.pop(0))
    while True:
        if "wild" in discards[-1] or "reverse" in discards[-1] or "skip" in discards[-1] or "drawtwo" in discards[-1]:
            discards.append(unoDeck.pop(0))
        else:
            break
    splitCard = discards[-1].split()
    currentColor = splitCard[0]
    if currentColor != "wild":
        cardVal = splitCard[1]
    else:
        cardVal = "Any"
    presentCard = discards[-1].split()
    currentColor = presentCard[0]
    print(Fore.WHITE + "card on top of discard pile: {}".format(discards[-1]))
    if len(presentCard) == 1:
        cardVal = "Any"
    else:
        cardVal = presentCard[1]


    while playing:
        players[playerTurn] = sorted(players[playerTurn], key=lambda x: x.split()[0])
        show_hand(playerTurn, players[playerTurn], names)
        print(Fore.WHITE + "card on top of discard pile: {}".format(discards[-1]))
        if can_play(currentColor, cardVal, players[playerTurn]):
            cardChosen = int(input(Fore.WHITE + "which card do you want to play?-->"))
            while not can_play(currentColor, cardVal, [players[playerTurn][cardChosen - 1]]):
                cardChosen = int(input(Fore.WHITE + "not a valid card. Which card do you want to choose? -->"))
            print(Fore.WHITE + "you played {}".format(players[playerTurn][cardChosen - 1]))
            discards.append(players[playerTurn].pop(cardChosen - 1))
            while True and "wild" not in discards[-1]:
                if can_add_card(discards[-1].split()[1], players[playerTurn]):
                    show_hand(playerTurn, players[playerTurn], names)
                    choose = int(input(Fore.WHITE + "you can also draw another card (or) To continue press - 0 -->"))
                    if choose == 0:
                        break
                    while not can_add_card(discards[-1].split()[1], [players[playerTurn][choose - 1]]):
                        choose = int(input(Fore.WHITE + "not a valid card. Which card do you want to choose? -->"))
                    print(Fore.WHITE + "you played {}".format(players[playerTurn][choose - 1]))
                    discards.append(players[playerTurn].pop(choose - 1))
                else:
                    break
            if len(players[playerTurn]) == 0:
                playing = False
                print(Fore.WHITE + "Player {} is WINNER!!!!!!!!!!".format(playerTurn+1))
                break
        else:
            print(Fore.WHITE + "You can't play, you have to draw a card -->")
            try:
                players[playerTurn] += cards_drawn(1)
            except Exception:
                unoDeck = shuffle_deck(discards[:-1])
                discards = [discards[-1]]
            show_hand(playerTurn, players[playerTurn], names)
            if can_play(currentColor, cardVal, players[playerTurn]):
                cardChosen = int(
                    input(Fore.WHITE + "you can now play a card, which card do you want to play?-->"))
                while not can_play(currentColor, cardVal, [players[playerTurn][cardChosen - 1]]):
                    cardChosen = int(input(Fore.WHITE + "not a valid card. Which card do you want to choose? -->"))
                print(Fore.WHITE + "you played {}".format(players[playerTurn][cardChosen - 1]))
                discards.append(players[playerTurn].pop(cardChosen - 1))
            else:
                time.sleep(2)
                player_increment()
                continue
        presentCard = discards[-1].split()
        currentColor = presentCard[0]
        if len(presentCard) == 1:
            cardVal = "Any"
        else:
            cardVal = presentCard[1]
        if currentColor == "wild":
            wild()
        if cardVal == "reverse":
            reverse()
        elif cardVal == "skip":
            skip()
        elif cardVal == "drawtwo":
            draw(2)
            players[playerTurn] = sorted(players[playerTurn], key=lambda x: x.split()[0])
        elif cardVal == "drawfour":
            draw(4)
            players[playerTurn] = sorted(players[playerTurn], key=lambda x: x.split()[0])
        print("")
        player_increment()
    ask = input(Fore.WHITE + "Do you wanna play again - Y or N -->").upper()
    if ask == "N":
        print(Fore.WHITE + "Thank you for playing!!!!!")
        break
print(Fore.WHITE + "thank you play again !!")
