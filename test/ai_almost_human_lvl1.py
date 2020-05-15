#cd..\src & python3 setup.py install --user & cd ..\test
from hanabi.ai import AI
from hanabi.deck import Color
from random import randint

class Robot_1(AI):
    "This robot follows human conventions"
    "Dans un premier temps, seulement fonctionnel pour des parties à 2 joueurs"

    def __init__(self, game, quiet=False):
        self.game = game
        self.quiet = quiet

    def play(self):
        game = self.game
    #    print(game.examine_piles())
        self.log("Is the situation risky ? ",self.situation_is_risky())
        (res,clues) = self.have_clue()
        if self.situation_is_risky():
            pass
        if res:
            for ind_card in range(len(game.current_hand.cards)-1,-1,-1):
                card = game.current_hand.cards[ind_card]
         #       if clues[ind_card][1] == '1':
                if (card.number_clue[0] == '1') & ( ( (not card.color_clue[0]) & (not card.bomb) ) or ( (not(not card.color_clue[0])) & ( card.number_clue[0] == (self.playable(card)) ) ) ) :
                    return("p%d"%(ind_card+1))
                if ( not(not card.color_clue[0])) & (not(not card.number_clue[0]) ):
                    if self.playable(card):
                        return("p%d"%(ind_card+1))
                if ( not(not card.color_clue[0])) & (not card.bomb) & (not card.number_clue[0]):
                    return("p%d"%(ind_card+1))
        if game.blue_coins > 0:
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
                    if self.playable(card) & (not card.color_clue[0]):
                        if (not self.conflit(hand,ind_card,str(card.color)[0])):
                            return("c%c"%(str(card.color)[0]))                            
                    if ((card.number == 5) & (not card.number_clue[0])):
                        if (not self.conflit(hand,ind_card,"5")):
                            return("c5")           
        if game.blue_coins == 8:
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
            self.log("give a random clue")
            return("c%d"%(randint(1,5)))
        self.log("Robot should discard")
        for ind_card in range(0,len(game.current_hand.cards)):
            card = game.current_hand.cards[ind_card]
            if card.color_clue:
                if game.piles[card.color] == 5:
                    return ("d%d"%(ind_card+1))
            if card.number_clue:
                if card.number < self.min_piles():
                    return ("d%d"%(ind_card+1))

        for ind_card in range(0,len(game.current_hand.cards)):            
            if clues[ind_card] == [None,None]:
              return("d%d"%(ind_card+1))
        return("d1")

    def have_clue(self): # retourne un booléen et un tableau d'indication
        game = self.game
        res = False
        clues = [[None,None],[None,None],[None,None],[None,None],[None,None]] #tableau de couples (indice couleur,indice nombre), FIX ME : utile ou card.number_clue et card.color_clue suffisent ?
        clue_is_bomb = False
        for ind_card in range(len(game.current_hand.cards)-1,-1,-1):
            card = game.current_hand.cards[ind_card]
            if card.color_clue[0]:
#                print(card," has a color clue")
                res = True
                card.color_clue[1] += 1
                clues[ind_card][0] = card.color_clue[0]
                if card.color_clue[1] == 1:
                    if clue_is_bomb & (not card.number_clue[0]):
                        card.bomb = True
                    clue_is_bomb = True
            if card.number_clue[0]:
#                print(card," has a number clue")
                res = True
                card.number_clue[1] += 1
                clues[ind_card][1] = card.number_clue[0]
                if card.number_clue[1] == 1:
                    if clue_is_bomb & (not card.color_clue[0]):
                        card.bomb = True
                    clue_is_bomb = True
        return(res,clues)

    def playable(self,card): # retourne si la carte peut être jouée sans risque
        game = self.game
        return(card.number == (game.piles[card.color]+1))

    def situation_is_risky(self): # retourne si une carte clef risque d'être défaussée par un partenaire
        game = self.game
        for ind_hand in range(0,len(self.other_hands)):
            hand = self.other_hands[ind_hand]
            chop_card = hand.cards[0]
            ind_card = 0
            while ((chop_card.number_clue[0] != False) & (ind_card<(len(hand.cards)-1))):
                ind_card += 1
                chop_card = hand.cards[ind_card]
            if (ind_card == 4) & (not(not(chop_card.number_clue[0]))):
                return(self.last_rep(hand.cards[0]))
            return(self.last_rep(chop_card))

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

    def log(self, *args, **kwargs):
        if self.quiet:
            pass
        else:
            print(*args, **kwargs)
        