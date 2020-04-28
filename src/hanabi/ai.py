"""
Artificial Intelligence to play Hanabi.
"""

import itertools


class AI:
    """
    AI base class: some basic functions, game analysis.
    """
    def __init__(self, game):
        self.game = game

    @property
    def other_hands(self):
        "The list of other players' hands."
        return self.game.hands[1:]

    @property
    def other_players_cards(self):
        "All of other players's cards, concatenated in a single list."
        # return sum([x.cards for x in self.other_hands], [])
        return list(itertools.chain.from_iterable([hand.cards for hand in self.other_hands]))




class Cheater(AI):
    """
    This player can see his own cards!

    Algorithm:
      * if 1-or-more card is playable: play the lowest one, then newest one
      * if blue_coin<8 and an unnecessary card present: discard it.
      * if blue_coin>0: give a clue on precious card (so a human can play with a Cheater)
      * if blue_coin<8: discard the largest one, except if it's the last of its kind or in chop position in his opponent.
    """

    def play(self):
        "Return the best cheater action."
        game = self.game
        playable = [ (i+1, card.number) for (i, card) in
                     enumerate(game.current_hand.cards)
                     if game.piles[card.color]+1 == card.number ]

        if playable:
            # sort by ascending number, then newest
            playable.sort(key=lambda p: (p[1], -p[0]))
            print('Cheater would play:', "p%d"%playable[0][0], end=' ')
            if (len(playable) > 1):
                print('but could also pick:', playable[1:])
            else:
                print()

            return "p%d"%playable[0][0]

        #
        discardable = [ i+1 for (i, card) in
                        enumerate(game.current_hand.cards)
                        if ( (card.number <= game.piles[card.color])
                             or (game.current_hand.cards.count(card) > 1)
                        ) ]
        # discard already played cards, doubles in my hand
        # fixme: discard doubles, if I see it in partner's hand
        # fixme: il me manque les cartes sup d'une pile morte

        if discardable and (game.blue_coins < 8):
            print('Cheater would discard:', "d%d"%discardable[0], discardable)
            return "d%d"%discardable[0]

        ## 2nd type of discard: I have a card, and my partner too

        discardable2 = [ i+1 for (i, card) in enumerate(game.current_hand.cards)
                         if card in self.other_players_cards
                       ]
        if discardable2 and (game.blue_coins < 8):
            print('Cheater would discard2:', "d%d"%discardable2[0], discardable2)
            return "d%d"%discardable2[0]


        ## Look at precious cards in other hand, to clue them
        precious = [ card for card in
                     self.other_players_cards
                     if (1+game.discard_pile.cards.count(card))
                         == game.deck.card_count[card.number]
                   ]
        if precious:
            clue = False
            # this loop is such that we prefer to clue an card close to chop
            # would be nice to clue an unclued first, instead of a already clued
            for p in precious:
                # print(p, p.number_clue, p.color_clue)
                if p.number_clue is False:
                    clue = "c%d"%p.number
                    break
                if p.color_clue is False:
                    clue = "c%s"%p.color
                    clue = clue[:2]   # quick fix, with 3+ players, can't clue cRed anymore, only cR
                    break
                # this one was tricky:
                # don't want to give twice the same clue
            if clue:
                print('Cheater would clue a precious:',
                       clue, precious)
                if game.blue_coins > 0:
                    return clue
                print("... but there's no blue coin left!")


        # if reach here, can't play, can't discard safely, no card to clue-save
        # Let's give a random clue, to see if partner can unblock me
        if game.blue_coins > 0:
            print('Cheater would clue randomly: cW')
            return 'cw'

        # If reach here, can't play, can't discard safely
        # No blue-coin left.
        # Must discard a card. Let's choose a non-precious one (preferably a 4)
        mynotprecious = [ (card.number, i+1) for (i, card) in
                          enumerate(game.current_hand.cards)
                          if not (
                                  (1+game.discard_pile.cards.count(card))
                                  == game.deck.card_count[card.number])
                     ]
        mynotprecious.sort(key=lambda p: (-p[0], p[1]))
        if mynotprecious:
            act = 'd%d'%mynotprecious[0][1]
            print('Cheater is trapped and must discard:', act, mynotprecious)
            return act

        # Oh boy, not even a safe discard, this is gonna hurt!
        # it's a loss. Discard the biggest
        myprecious = [ (card.number, i+1) for (i, card) in enumerate(game.current_hand.cards) ]
        myprecious.sort(key=lambda p: (-p[0], p[1]))
        act = 'd%d'%myprecious[0][1]
        print('Cheater is doomed and must discard:', act, myprecious)
        return act


class Robot_thinking_as_human(AI):
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
                    if ((card.number == 1) & (not card.number_clue) & (game.piles[card.color] == 0)):
                        return ("c1")
                    if ((card.number == 5) & (not card.number_clue)):
                       return("c5")                        
            if game.blue_coins == 8:
                return("c2")
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
            if card.color_clue:
                res = True
                clues[ind_card][0] = card.color_clue
            if card.number_clue:
                res = True
                clues[ind_card][1] = card.number_clue
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
            while ((chop_card.number_clue != False) & (ind_card<(len(hand.cards)-1))):
                ind_card += 1
                chop_card = hand.cards[ind_card]
            if (ind_card == 4 & chop_card.number_clue):
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
