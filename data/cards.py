from settings import *

import random

class Cards:

    def __init__(self, index, rank, suit, emoji, link):
        self.index = index # Might as well replace it with value simply
        self.rank = rank
        self.suit = suit
        self.emoji = emoji
        self.link = link
        # self.value = value (a = 14, 2 = 2, k = 13)
    
c1s = Cards(1, "A", "spades", E_SPADES, "https://cdn.discordapp.com/attachments/849521016073224212/849521513379266570/AS.png")
c2s = Cards(2, "2", "spades", E_SPADES, "https://cdn.discordapp.com/attachments/849521016073224212/849523390761926696/2S.png")
c3s = Cards(3, "3", "spades", E_SPADES, "https://cdn.discordapp.com/attachments/849521016073224212/849523416663195678/3S.png")
c4s = Cards(4, "4", "spades", E_SPADES, "https://cdn.discordapp.com/attachments/849521016073224212/849523434840260618/4S.png")
c5s = Cards(5, "5", "spades", E_SPADES, "https://cdn.discordapp.com/attachments/849521016073224212/849523460614520912/5S.png")
c6s = Cards(6, "6", "spades", E_SPADES, "https://cdn.discordapp.com/attachments/849521016073224212/849523528952840202/6S.png")
c7s = Cards(7, "7", "spades", E_SPADES, "https://cdn.discordapp.com/attachments/849521016073224212/849523560108261386/7S.png")
c8s = Cards(8, "8", "spades", E_SPADES, "https://cdn.discordapp.com/attachments/849521016073224212/849523588536336424/8S.png")
c9s = Cards(9, "9", "spades", E_SPADES, "https://cdn.discordapp.com/attachments/849521016073224212/849523716903403541/9S.png")
c10s = Cards(10, "10", "spades", E_SPADES, "https://cdn.discordapp.com/attachments/849521016073224212/849523741721231410/10S.png")
c11s = Cards(11, "J", "spades", E_SPADES, "https://cdn.discordapp.com/attachments/849521016073224212/849523789700399114/JS.png")
c12s = Cards(12, "Q", "spades", E_SPADES, "https://cdn.discordapp.com/attachments/849521016073224212/849523832892293180/QS.png")
c13s = Cards(13, "K", "spades", E_SPADES, "https://cdn.discordapp.com/attachments/849521016073224212/849523860839858186/KS.png")
c1h = Cards(1, "A", "hearts", E_HEARTS, "https://cdn.discordapp.com/attachments/849521016073224212/849523937574256710/AH.png")
c2h = Cards(2, "2", "hearts", E_HEARTS, "https://cdn.discordapp.com/attachments/849521016073224212/849524049109712916/2H.png")
c3h = Cards(3, "3", "hearts", E_HEARTS, "https://cdn.discordapp.com/attachments/849521016073224212/849524052136558612/3H.png")
c4h = Cards(4, "4", "hearts", E_HEARTS, "https://cdn.discordapp.com/attachments/849521016073224212/849524055514021918/4H.png")
c5h = Cards(5, "5", "hearts", E_HEARTS, "https://cdn.discordapp.com/attachments/849521016073224212/849524158978588692/5H.png")
c6h = Cards(6, "6", "hearts", E_HEARTS, "https://cdn.discordapp.com/attachments/849521016073224212/849524162363654154/6H.png")
c7h = Cards(7, "7", "hearts", E_HEARTS, "https://cdn.discordapp.com/attachments/849521016073224212/849524166554157086/7H.png")
c8h = Cards(8, "8", "hearts", E_HEARTS, "https://cdn.discordapp.com/attachments/849521016073224212/849524204821938256/8H.png")
c9h = Cards(9, "9", "hearts", E_HEARTS, "https://cdn.discordapp.com/attachments/849521016073224212/849524207921922068/9H.png")
c10h = Cards(10, "10", "hearts", E_HEARTS, "https://cdn.discordapp.com/attachments/849521016073224212/849524296916140032/10H.png")
c11h = Cards(11, "J", "hearts", E_HEARTS, "https://cdn.discordapp.com/attachments/849521016073224212/849524303283355678/JH.png")
c12h = Cards(12, "Q", "hearts", E_HEARTS, "https://cdn.discordapp.com/attachments/849521016073224212/849524383332433930/QH.png")
c13h = Cards(13, "K", "hearts", E_HEARTS, "https://cdn.discordapp.com/attachments/849521016073224212/849524408254332949/KH.png")
c1d = Cards(1, "A", "diamonds", E_DIAMONDS, "https://cdn.discordapp.com/attachments/849521016073224212/849525162391240714/AD.png")
c2d = Cards(2, "2", "diamonds", E_DIAMONDS, "https://cdn.discordapp.com/attachments/849521016073224212/849525205407760434/2D.png")
c3d = Cards(3, "3", "diamonds", E_DIAMONDS, "https://cdn.discordapp.com/attachments/849521016073224212/849525257337307136/3D.png")
c4d = Cards(4, "4", "diamonds", E_DIAMONDS, "https://cdn.discordapp.com/attachments/849521016073224212/849525280967753788/4D.png")
c5d = Cards(5, "5", "diamonds", E_DIAMONDS, "https://cdn.discordapp.com/attachments/849521016073224212/849525284419272704/5D.png")
c6d = Cards(6, "6", "diamonds", E_DIAMONDS, "https://cdn.discordapp.com/attachments/849521016073224212/849525394599051264/6D.png")
c7d = Cards(7, "7", "diamonds", E_DIAMONDS, "https://cdn.discordapp.com/attachments/849521016073224212/849525396889141290/7D.png")
c8d = Cards(8, "8", "diamonds", E_DIAMONDS, "https://cdn.discordapp.com/attachments/849521016073224212/849525471238553630/8D.png")
c9d = Cards(9, "9", "diamonds", E_DIAMONDS, "https://cdn.discordapp.com/attachments/849521016073224212/849525475889643530/9D.png")
c10d = Cards(10, "10", "diamonds", E_DIAMONDS, "https://cdn.discordapp.com/attachments/849521016073224212/849525482709844018/10D.png")
c11d = Cards(11, "J", "diamonds", E_DIAMONDS, "https://cdn.discordapp.com/attachments/849521016073224212/849525510593708032/JD.png")
c12d = Cards(12, "Q", "diamonds", E_DIAMONDS, "https://cdn.discordapp.com/attachments/849521016073224212/849525554134777906/QD.png")
c13d = Cards(13, "K", "diamonds", E_DIAMONDS, "https://cdn.discordapp.com/attachments/849521016073224212/849525608660729866/KD.png")
c1c = Cards(1, "A", "clubs", E_CLUBS, "https://cdn.discordapp.com/attachments/849521016073224212/849525759945342976/AC.png")
c2c = Cards(2, "2", "clubs", E_CLUBS, "https://cdn.discordapp.com/attachments/849521016073224212/849525790105403393/2C.png")
c3c = Cards(3, "3", "clubs", E_CLUBS, "https://cdn.discordapp.com/attachments/849521016073224212/849525832912601098/3C.png")
c4c = Cards(4, "4", "clubs", E_CLUBS, "https://cdn.discordapp.com/attachments/849521016073224212/849526039881187338/4C.png")
c5c = Cards(5, "5", "clubs", E_CLUBS, "https://cdn.discordapp.com/attachments/849521016073224212/849526042321354782/5C.png")
c6c = Cards(6, "6", "clubs", E_CLUBS, "https://cdn.discordapp.com/attachments/849521016073224212/849526092779094037/6C.png")
c7c = Cards(7, "7", "clubs", E_CLUBS, "https://cdn.discordapp.com/attachments/849521016073224212/849526094708080660/7C.png")
c8c = Cards(8, "8", "clubs", E_CLUBS, "https://cdn.discordapp.com/attachments/849521016073224212/849526121128656946/8C.png")
c9c = Cards(9, "9", "clubs", E_CLUBS, "https://cdn.discordapp.com/attachments/849521016073224212/849526121280176148/9C.png")
c10c = Cards(10, "10", "clubs", E_CLUBS, "https://cdn.discordapp.com/attachments/849521016073224212/849526196022411295/10C.png")
c11c = Cards(11, "J", "clubs", E_CLUBS, "https://cdn.discordapp.com/attachments/849521016073224212/849526218867998723/JC.png")
c12c = Cards(12, "Q", "clubs", E_CLUBS, "https://cdn.discordapp.com/attachments/849521016073224212/849526235016724480/QC.png")
c13c = Cards(13, "K", "clubs", E_CLUBS, "https://cdn.discordapp.com/attachments/849521016073224212/849526287302131762/KC.png")

class Deck:
    def __init__(self):
        self.deck = ([
            c1s, c2s, c3s, c4s, c5s, c6s, c7s, c8s, c9s, c10s, c11s, c12s, c13s,
            c1h, c2h, c3h, c4h, c5h, c6h, c7h, c8h, c9h, c10h, c11h, c12h, c13h,
            c1d, c2d, c3d, c4d, c5d, c6d, c7d, c8d, c9d, c10d, c11d, c12d, c13d,
            c1c, c2c, c3c, c4c, c5c, c6c, c7c, c8c, c9c, c10c, c11c, c12c, c13c
        ])
        random.shuffle(self.deck)

    # The method to distribute cards to a player from a deck
    # This method returns a hand (list) that can also be appended to existing hand (existing list)
    def distribute(self, number):
        hand = []       # The list, that'll be returned
        for i in range(number):        # Pops the cards from the deck "number" number of times and adds it to the hand
            hand.append(self.deck.pop())

        return hand        # The hand is returned, now we can do anything with this list of hand that is returned