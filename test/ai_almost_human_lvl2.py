#cd..\src & python3 setup.py install --user & cd ..\test
from hanabi.ai import AI
from hanabi.deck import Color
from random import randint

class Robot_2(AI):
    "This robot follows human conventions"
    "Dans un premier temps, seulement fonctionnel pour des parties à 2 joueurs"

    def __init__(self, game, quiet=False):
        self.game = game
        self.quiet = quiet

    def play(self):
        game = self.game
        self.log(game.examine_piles())
        self.log("Is the situation risky ? ",self.situation_is_risky())

        if self.situation_is_risky() & (game.blue_coins > 0):
            ind_chop_card = self.situation_is_risky()
            if not self.possibly_playable((self.other_hands[0].cards[ind_chop_card]).number):
                return("c%d"%ind_chop_card)
            if self.give_playable_clue() != None:
                return(self.give_playable_clue())
            if self.give_discardable_clue() != None:
                return(self.give_discardable_clue())
      #      if self.give_punish_clue() != None:
     #           return(self.give_punish_clue())
        res = self.have_clue()
        if res:
            if self.play_card_safely() != None:
                return(self.play_card_safely())
        if game.blue_coins > 0:
            if self.give_playable_clue() != None:
                return(self.give_playable_clue())

        if game.blue_coins == 8:
            if self.give_discardable_clue() != None:
                return(self.give_discardable_clue())
            return(self.give_random_clue())
        return(self.discard_at_all_costs(game.current_hand))

    def have_clue(self): # retourne un booléen et un tableau d'indication
        game = self.game
        res = False
        clue_is_bomb = False #perme de savoir quel indice est celui pertinent et lesquels sont des bombes
        for ind_card in range(len(game.current_hand.cards)-1,-1,-1):
            card = game.current_hand.cards[ind_card]
            if card.color_clue[0]:
#                print(card," has a color clue")
                res = True
                card.color_clue[1] += 1
                if card.color_clue[1] == 1:
                    if clue_is_bomb & (not card.number_clue[0]):
                        card.bomb = True
                    clue_is_bomb = True
            if card.number_clue[0]:
#                print(card," has a number clue")
                res = True
                card.number_clue[1] += 1
                if card.number_clue[1] == 1:
                    if clue_is_bomb & (not card.color_clue[0]):
                        card.bomb = True
                    clue_is_bomb = True
        return(res)

    def is_playable(self,card): # retourne si la carte peut être jouée sans risque
        game = self.game
        return(card.number == (game.piles[card.color]+1))

    def play_card_safely(self):
        game = self.game
        for ind_card in range(len(game.current_hand.cards)-1,-1,-1):
            card = game.current_hand.cards[ind_card]
            if (card.number_clue[0] == '1') & (self.min_piles == 0) & ( ( (not card.color_clue[0]) & (not card.bomb) ) or ( (not(not card.color_clue[0])) & ( card.number_clue[0] == (self.is_playable(card)) ) ) ) :
                return("p%d"%(ind_card+1))
            if ( not(not card.color_clue[0])) & (not(not card.number_clue[0]) ):
                if self.is_playable(card):
                    return("p%d"%(ind_card+1))
            if ( not(not card.color_clue[0])) & (not card.bomb) & (not card.number_clue[0]):
                return("p%d"%(ind_card+1))

    def give_playable_clue(self):
        game = self.game
        for ind_hand in range(len(self.other_hands)-1,-1,-1):
            hand = self.other_hands[ind_hand]
            for ind_card in range(0,len(hand.cards)):
                card = hand.cards[ind_card]
    #                    print(card," is a bomb ? ",card.bomb)
                if ((card.number == 1) & (game.piles[card.color] == 0)):
                    if (not card.number_clue[0]):
                        if (not self.conflit(hand,ind_card,"1")):
                            return ("c1")
                        if (not card.color_clue[0]) & (not self.conflit(hand,ind_card,str(card.color)[0])):
                            return ("c%c"%(str(card.color)[0]))
                    if (not self.conflit(hand,ind_card,str(card.color)[0])) & (not(card.color_clue[0])) & card.bomb:
                        return ("c"+str(card.color)[0])
                if self.is_playable(card) & (not card.color_clue[0]):
                    if (not self.conflit(hand,ind_card,str(card.color)[0])):
                        return("c%c"%(str(card.color)[0]))                            
                if ((card.number == 5) & (not card.number_clue[0])):
                    if (not self.conflit(hand,ind_card,"5")):
                        return("c5")

    def give_discardable_clue(self):
        game = self.game
        for ind_hand in range(len(self.other_hands)-1,-1,-1):
            hand = self.other_hands[ind_hand]
            for ind_card in range(0,len(hand.cards)):
                card = hand.cards[ind_card]
                if card.number < self.min_piles():
                    self.log("cardnumb < min pile",card)
                    return ("c%d"%(card.number))
                if card.color_clue:
                    if game.piles[card.color] == 5:
                        self.log("cardcolor is full",card)
                        return ("c%s"%(str(card.color)[0]))

    def give_punish_clue(self):
        return()

    def give_random_clue(self):
        self.log("give a random clue")
        return("c%d"%(randint(1,5)))

    def discard_safely(self,hand):
        game = self.game
        for ind_card in range(0,len(hand.cards)):
            card = hand.cards[ind_card]
            if card.color_clue:
                if game.piles[card.color] == 5:
                    return ("d%d"%(ind_card+1))
            if card.number_clue:
                if card.number < self.min_piles():
                    return ("d%d"%(ind_card+1))        

    def discard_at_all_costs(self,hand):
        game = self.game
        for ind_card in range(0,len(hand.cards)):
            card = hand.cards[ind_card]
            if card.color_clue:
                if game.piles[card.color] == 5:
                    return ("d%d"%(ind_card+1))
            if card.number_clue:
                if card.number < self.min_piles():
                    return ("d%d"%(ind_card+1))
        for ind_card in range(0,len(hand.cards)):
            card = hand.cards[ind_card]
            if (not card.color_clue) & (not card.number_clue):
              return("d%d"%(ind_card+1))
        return("d1")

    def situation_is_risky(self): # retourne si une carte clef risque d'être défaussée par un partenaire
        game = self.game
        for ind_hand in range(0,len(self.other_hands)):
            hand = self.other_hands[ind_hand]
        #     chop_card = hand.cards[0]
        #     ind_card = 0
        #     while ((chop_card.number_clue[0] != False) & (ind_card<(len(hand.cards)-1))):
        #         ind_card += 1
        #         chop_card = hand.cards[ind_card]
        #     if (ind_card == 4) & (not(not(chop_card.number_clue[0]))):
        #         return(self.last_rep(hand.cards[0]))
        #     return(self.last_rep(chop_card))
            ind_chop_card = int(self.discard_at_all_costs(hand)[1])-1
            if (self.last_rep( hand.cards[ ind_chop_card ] )):
                return(ind_chop_card)
            return(False)

    def last_rep(self,card): # retourne si la carte n'a pas encore été posée et qu'elle est la dernière disponible
        game = self.game
        if card.number == 5:
            return(True)
        if card.number > 1:
            return(card in game.discard_pile.cards)
        if card.number == 1:
            return(game.discard_pile.cards.count(card) == 2)

    def conflit(self,hand,ind_card,c):
        game = self.game
       # if ind_card == len(hand.cards - 1):
     #       return False
        for i in range(ind_card + 1,len(hand.cards)):
            if (str(hand.cards[i].number) == c) or (str(hand.cards[i].color)[0] == c):
                return True
        return False

    def min_piles(self):
        game = self.game
        min = None
        for color in list(Color):
            if (min is None) or (game.piles[color] < min):
                min = game.piles[color]
        return(min)

    def possibly_playable(self,value):
        game = self.game
        for color in list(Color):
                if game.piles[color] == value - 1:
                    return(True)
        return(False)

    def log(self, *args, **kwargs):
        if self.quiet:
            pass
        else:
            print(*args, **kwargs)