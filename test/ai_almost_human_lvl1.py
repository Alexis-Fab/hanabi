from hanabi.ai import AI
from random import randint

class Robot_1(AI):
    "This robot follows human conventions"
    "Dans un premier temps, seulement fonctionnel pour des parties à 2 joueurs"

    def play(self):
        game = self.game
        print(game.examine_piles())
        print("Is the situation risky ? ",self.situation_is_risky())
        (res,clues) = self.have_clue()
        if res:
            for ind_card in range(0,len(game.current_hand.cards)):
                if clues[ind_card][1] == '1':
                    return("p%d"%(ind_card+1))
        if game.blue_coins > 0:
            for ind_hand in range(0,len(self.other_hands)):
                hand = self.other_hands[ind_hand]
                for ind_card in range(0,len(hand.cards)):
                    card = hand.cards[ind_card]
                    if ((card.number == 1) & (not card.number_clue[0]) & (game.piles[card.color] == 0)):
                        return ("c1")
                    if ((card.number == 5) & (not card.number_clue[0])):
                       return("c5")
            if game.blue_coins == 8:
                return("c%d"%(randint(2,5)))
        print("Robot should discard")
        for ind_card in range(0,len(game.current_hand.cards)):
            if clues[ind_card] == [None,None]:
              return("d%d"%(ind_card+1))
        return("d1")

    def have_clue(self): # retourne un booléen et un tableau d'indication
        game = self.game
        res = False
        clues = [[None,None],[None,None],[None,None],[None,None],[None,None]] #tableau de couples (indice couleur,indice nombre), FIX ME : utile ou card.number_clue et card.color_clue suffisent ?
        for ind_card in range(0,len(game.current_hand.cards)):
            card = game.current_hand.cards[ind_card]
            if card.color_clue[0]:
                res = True
                clues[ind_card][0] = card.color_clue[0]
            if card.number_clue[0]:
                res = True
                clues[ind_card][1] = card.number_clue[0]
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
                if (ind_card == 4 & int(chop_card.number_clue[0])):
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
