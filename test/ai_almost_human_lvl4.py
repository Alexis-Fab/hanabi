#cd..\src & python3 setup.py install --user & cd ..\test
from hanabi.ai import AI
from hanabi.deck import Color
from random import randint

class Robot_4(AI):
    "This robot follows human conventions"
    "Dans un premier temps, seulement fonctionnel pour des parties à 2 joueurs"

    def __init__(self, game, quiet=False):
        self.game = game
        self.quiet = quiet

    def play(self):
        game = self.game
        #self.log(game.examine_piles())
        have_clue = self.have_clue()

        for ind_card in range(len(game.current_hand.cards)-1,-1,-1):
            card = game.current_hand.cards[ind_card]
            if card.bomb:
                self.log(card,"=bomb")
                pass

        for ind_card in range(len(game.current_hand.cards)-1,-1,-1):
            card = game.current_hand.cards[ind_card]
            if (card.number_clue[0] or card.color_clue[0]) and card.bomb == False:
                self.log(card,"=indice pertinent")
                pass

        self.set_crucial_cards() # cela identifie les cartes cruciales, nécessite d'avoir mis à jour les indices (have_clue)

        self.log("partner hand" , str(self.other_hands[0]))
        if self.try_to_play_a_bomb(self.other_hands[0]) and (self.try_to_play_card_safely(self.other_hands[0]) is None):
            self.log(self.try_to_play_a_bomb(self.other_hands[0]))
            ind_other_discard_card=int(self.try_to_play_a_bomb(self.other_hands[0])[1])-1
            if not self.is_playable(self.other_hands[0].cards[ind_other_discard_card]):
                self.log("Robot saves a bomb")
                self.try_to_save_a_bomb()

        risk = self.situation_is_risky()
        #self.log("risk is",risk)
        self.log("Is the situation risky ? ",risk != False) #FIX ME rajouter les bombes jouées au prochain tour dans risky <-- elles sont déjà prises en compte
        if (risk != False) & (game.blue_coins > 0):
            self.log("situation is risky")
            ind_chop_card = risk
            if not self.possibly_playable((self.other_hands[0].cards[ind_chop_card]).number): # ie chop_card la carte FIX ME ceci n'est pas la carte qui sera défaussée !!! si ce n'est pas le cas, il faudra utiliser punish
                #self.log("Robot saves playable chop card")
                return("c%d"%(self.other_hands[0].cards[0]).number)
            if self.give_relevant_clue() != None:
                #self.log("Robot gives a playable clue")
                return(self.give_relevant_clue())
            if self.give_discardable_clue() != None:
                #self.log("Robot gives a discardable clue")
                return(self.give_discardable_clue())
      #      if self.give_punish_clue() != None:     FIX ME à écrire, attention différence entre carte qui sera défaussée et carte à côté du punish
     #           return(self.give_punish_clue())

        #self.log("Robot possède des indices ? ",have_clue)
        if have_clue:
            temp = self.try_to_play_card_safely(game.current_hand)
            #self.log("play_safely = ",temp)
            if temp != None:
                self.log("Robot plays safely")
                return(temp)
        if game.blue_coins > 0:
            temp = self.give_relevant_clue()
            if temp != None:
                #self.log("Robot gives a playable clue or saves a bomb")
                return(temp)

        temp = self.try_to_play_a_bomb(game.current_hand)
        if temp != None:
            self.log("Robot tries to play a bomb")
            return(temp)

        if game.blue_coins == 8:
            temp = self.give_discardable_clue()
            if temp != None:
                #self.log("Robot gives a discardable clue")
                return(temp)
            self.log("Robot gives a random clue") # FIX ME réfléchir à une optimisation
            return(self.give_random_clue())
        self.log("Robot should discard")
        return(self.discard_at_all_costs(game.current_hand))

    def have_clue(self):
        """Retourne un booleen indiquant si le robot a des indices, et détermine les bombes de son jeu en les analysant"""
       # self.log("Robot looks for clues")
        game = self.game
        res = False
        clue_is_bomb = False #permet de savoir quel indice est celui pertinent et lesquels sont des bombes
        for ind_card in range(len(game.current_hand.cards)-1,-1,-1):
            card = game.current_hand.cards[ind_card]
            if card.color_clue[0]:
               # self.log(card," has a color clue")
                res = True
                card.color_clue[1] += 1
               # self.log(card,"has been given %d turns ago"%card.color_clue[1])
               # self.log("clue_is_bomb",clue_is_bomb)
                if card.color_clue[1] == 1:
                    if clue_is_bomb & (not card.number_clue[0]):
                        self.log(card,"is spotted as a bomb")
                        card.bomb = True
                    clue_is_bomb = True
                if card.number_clue[0]:
                   # self.log("robot reset bomb to False coz it knows the whole card")
                    card.bomb = False
            if card.number_clue[0] and card.number_clue[0] != '5':
               # self.log(card,"has a number clue")
                res = True
                card.number_clue[1] += 1
               # self.log(card,"has been given %d turns ago"%card.number_clue[1])
               # self.log("clue_is_bomb",clue_is_bomb)
                if card.number_clue[1] == 1:
                    if clue_is_bomb & (not card.color_clue[0]):
                        self.log(card,"is spotted as a bomb")
                        card.bomb = True
                    clue_is_bomb = True
                if card.color_clue[0]:
                   # self.log("robot reset bomb to False coz it knows the whole card")
                    card.bomb = False
            if card.crucial:
                card.bomb=False
      #  self.log("Robot knows its clues and spotted the bombs")
        return(res)

    def set_crucial_cards(self): #FIX ME comment savoir si la carte jouée précédemment était une punish ou si un random clue à été donné ? (ie comment avoir accès à l'historique des actions/résultats)
        
        """Détermine les cartes cruciales de son jeu qui ne doivent à aucun prix être défaussées"""
        game = self.game          # FIX ME les discardable cards ne doivent pas être cruciales !
        #self.log("robot sets the crucial cards")
        cards = game.current_hand.cards
        for ind_card in range(0,len(cards)):
            card=cards[ind_card]
            if (not card.crucial):
                if card.number_clue[0]:
                    if int(card.number_clue[0]) <= self.min_piles():
                        card.crucial = False
                    else:
                        if card.color_clue[0]:
                            card.crucial = self.last_rep(card)
                        if card.number_clue[0] == '5':
                            card.crucial = True
                        elif (card.number_clue[1] == 1) & (not self.possibly_playable(int(card.number_clue[0]))):
                            card.crucial = True
                            for ind_card2 in range(0,ind_card):
                                card2 = cards[ind_card2]
                                if (not card2.number_clue[0]) & (not card2.color_clue[0]):
                                    card2.crucial = True
            #if card.crucial:
                #self.log((card.color_clue[0] or '*') + (card.number_clue[0] or '*')," is crucial !")


    def is_playable(self,card): # retourne si la carte peut être jouée sans risque
        game = self.game
        return(card.number == (game.piles[card.color]+1))

    def try_to_play_card_safely(self,hand):
        """Joue une carte qui n'est pas une bombe si les indices indiquent de le faire"""
        game = self.game
        for ind_card in range(len(game.current_hand.cards)-1,-1,-1):
            card = game.current_hand.cards[ind_card]
            if (card.number_clue[0] == '1') and (self.min_piles() == 0) and ( ( (not card.color_clue[0]) and (not card.bomb) ) or (card.color_clue[0] and (self.is_playable(card)) )):
              
                #self.log("robot plays a 1")
                return("p%d"%(ind_card+1))
            if card.color_clue[0] and card.number_clue[0]:
                if self.is_playable(card):
                    #self.log("robot plays knows the color and the number of a playable card")
                    return("p%d"%(ind_card+1))
        for ind_card in range(len(game.current_hand.cards)-1,-1,-1):
            card = game.current_hand.cards[ind_card]
            if not (card.color_clue[0] and card.number_clue[0]):
      #          self.log(card.number_clue[0],self.min_piles(),card.color_clue[0],card.bomb,self.is_playable(card))
                if ( card.color_clue[0] or card.number_clue[0]) and (not card.bomb) and (not card.crucial):
                    
                    if card.number_clue[0] != False:
                        if self.possibly_playable(int(card.number_clue[0])):

                            other_first_bomb = None
                            indicateur_1 = None                                       #indique si la carte sélectionnée se trouve malheureusment être la prochaine bombe à être jouée par le partenaire: s'il joue la même après le robot, c'est red coin
                            for ind_other_hand in range(0,len(self.other_hands)):
                                other_hand = self.other_hands[ind_other_hand]
                                for ind_other_card in range(len(other_hand.cards)-1,-1,-1):
                                    other_card = other_hand.cards[ind_other_card]
                                    if (other_card.bomb and (indicateur_1 == None)):
                                        indicateur_1 = False
                                        other_first_bomb = other_card                     #indicateur indique que la première bombe en partant de la droite est atteinte mais que, pour l'instant, rien ne dit que c'est la même que celle que le robot veut jouer
                                        if (other_card.number_clue[0] == card.number_clue[0]):
                                            indicateur_1 = True
                                            #self.log("danger next bomb partenaire spotted")

                            indicateur_3 = False                                        #indque si la prochaine bombe du partenaire n'est pas jouable
                            if (other_first_bomb != None):
                                self.log(other_first_bomb, "est la prochaine bombe (safely)")
                                if (not self.is_playable(other_first_bomb)):
                                    indicateur_3 = True

                            if (indicateur_3 != True) and (card.number_clue != '5'):
                                self.log("applique indice pertinent du partenaire")
                                return("p%d"%(ind_card+1))
                    if card.color_clue[0] != False:
                        if game.piles[card.color] < 5:

                            other_first_bomb = None
                            indicateur_1 = None                                       #indique si la carte sélectionnée se trouve malheureusment être la prochaine bombe à être jouée par le partenaire: s'il joue la même après le robot, c'est red coin
                            for ind_other_hand in range(0,len(self.other_hands)):
                                other_hand = self.other_hands[ind_other_hand]
                                for ind_other_card in range(len(other_hand.cards)-1,-1,-1):
                                    other_card = other_hand.cards[ind_other_card]
                                    if (other_card.bomb and (indicateur_1 == None)):
                                        other_first_bomb = other_card
                                        indicateur_1 = False                          #indicateur indique que la première bombe en partant de la droite est atteinte mais que, pour l'instant, rien ne dit que c'est la même que celle que le robot veut jouer
                                        if (other_card.color_clue[0] == card.color_clue[0]):
                                            indicateur_1 = True
                                            self.log("danger next bomb partenaire spotted")

                            
                            indicateur_2 = False                                #indique un autre problème lié à la prochaine carte bombe du partenaire
                            if (other_first_bomb != None):                          
                                if (other_first_bomb.color == card.color) and (game.piles[card.color] + 2 != other_first_bomb.number):
                                    self.log("danger next bomb partenaire spotted")
                                    indicateur_2 = True

                            indicateur_3 = False
                            if (other_first_bomb != None):
                                self.log(other_first_bomb, "est la prochaine bombe (safely)")
                                if (not self.is_playable(other_first_bomb)):
                                    indicateur_3 = True

                            if (indicateur_2 != True) and (indicateur_3 != True):
                                self.log("applique indice pertinent du partenaire")
                                return("p%d"%(ind_card+1))

    def try_to_play_a_bomb(self,hand):
        """Joue une carte bombe si elle est jouable, en partant de la droite"""
        game = self.game
        for ind_card in range(len(game.current_hand.cards)-1,-1,-1):
            card = game.current_hand.cards[ind_card]
            if card.bomb:
                if card.number_clue[0]:
                    if self.possibly_playable(int(card.number_clue[0])):
                        return("p%d"%(ind_card+1))
                if card.color_clue[0]:
                    if game.piles[card.color] != 5:
                        return("p%d"%(ind_card+1))

    def try_to_save_a_bomb(self):
        game=self.game
        hand=self.other_hands[0]
        if self.try_to_play_a_bomb(hand):
            ind_bomb=int(self.try_to_play_a_bomb(hand)[1])-1
            card=hand.cards[ind_bomb]
            if (not card.color_clue[0]) & (not self.conflit(hand,ind_bomb,str(card.color)[0])):
                self.log("Robot saves a bomb")
                return("c%c"%(str(card.color)[0]))
            if (not card.number_clue[0]) & (not self.conflit(hand,ind_bomb,card.number)):
                self.log("Robot saves a bomb")
                return("c%d"%(card.number))




    def give_relevant_clue(self): #FIX ME give 5 clue even if chop_card is playable
        """Donne un indice au partenaire parmi : carte jouable, sauver une bombe, protéger un 5"""
        game = self.game
        choice = None
        bomb_choice = None
        bomb_card = None
        there_is_5 = False
        (nb_clues_given,nb_bombs_given) = (0,5)


        other_first_bomb = None
        indic = None                                       #indique si la carte sélectionnée se trouve malheureusment être la prochaine bombe à être jouée par le partenaire: s'il joue la même après le robot, c'est red coin
        for ind_other_hand in range(0,len(self.other_hands)):
            other_hand = self.other_hands[ind_other_hand]
            for ind_other_card in range(len(other_hand.cards)-1,-1,-1):
                other_card = other_hand.cards[ind_other_card]
                if (other_card.bomb and (indic == None)):
                    other_first_bomb = other_card
                    indic = True

        if (other_first_bomb != None):
            self.log(other_first_bomb, "est la prochaine bombe (give clue)")

        for ind_hand in range(0,len(self.other_hands)):
            hand = self.other_hands[ind_hand]
            for ind_card in range(len(hand.cards)-1,-1,-1):
                card = hand.cards[ind_card]
                if self.is_playable(card) & (not card.bomb): # & ((choice != "c5") or (card.number == 1))
                #    self.log(not card.color_clue[0],not self.conflit(hand,ind_card,str(card.color)[0]))
                    if (not card.color_clue[0]) & (not self.conflit(hand,ind_card,str(card.color)[0])):
                        (nb_clues,nb_bombs) = self.col_clue_score(hand,card)
                       # if (nb_clues,nb_bombs) == (0,5):
                           # self.log("%s is playable but col_clue would lead to another unplayable card being played before"%str(card))
                       # else:
                           # self.log("%s is playable and col_clue would lead to %d clues and %d bombs"%(str(card),nb_clues,nb_bombs))
                        if ( (nb_bombs < nb_bombs_given) & (nb_clues > 0) ) or ( (nb_bombs == nb_bombs_given) & (nb_clues > nb_clues_given) ):
                            (nb_clues_given,nb_bombs_given) = (nb_clues,nb_bombs)
                            choice = ("c%c"%(str(card.color)[0]))
                    if (not card.number_clue[0]) & (not self.conflit(hand,ind_card,card.number)):
                        (nb_clues,nb_bombs) = self.num_clue_score(hand,card)
                        #if (nb_clues,nb_bombs) == (0,5):
                           # self.log("%s is playable but num_clue would lead to another unplayable card being played before"%str(card))
                        #else:
                            #self.log("%s is playable and num_clue would lead to %d clues and %d bombs"%(str(card),nb_clues,nb_bombs))
                        if ( (nb_bombs < nb_bombs_given) & (nb_clues > 0) ) or ( (nb_bombs == nb_bombs_given) & (nb_clues > nb_clues_given) ):
                            (nb_clues_given,nb_bombs_given) = (nb_clues,nb_bombs)
                            choice = ("c%d"%(card.number))
                elif card.bomb & (not self.is_playable(card)):
                    if (not card.color_clue[0]) & (not self.conflit(hand,ind_card,str(card.color)[0])): # elle a donc un indice sur le nombre
                        if (other_first_bomb != None):
                            if (card == other_first_bomb):
                                bomb_choice = ("c%c"%(str(card.color)[0]))
                    if (not card.number_clue[0]) & (not self.conflit(hand,ind_card,card.number)): # elle a donc un indice sur la couleur
                        if (other_first_bomb != None):
                            if (card == other_first_bomb):
                                bomb_choice = ("c%d"%(card.number))

                if (card.number == 5) & (not card.number_clue[0]) & (not self.possibly_playable(5)) & (ind_card-2 < int(self.discard_at_all_costs(hand)[1]))-1:
                    if (not self.conflit(hand,ind_card,"5")):
                        #self.log("choice before 5 was %s"%choice)
                        there_is_5 = True

        
        if bomb_choice != None:
            self.log("robot saves a bomb")
            return(bomb_choice)
            
        if choice != None:
            res = False
            for ind_card in range(0,len(game.current_hand.cards)):
                card = game.current_hand.cards[ind_card]
                if ((card.color_clue[0] == choice[1]) or (card.number_clue[0] == choice[1])) and (card.bomb):
                    res = True
            if (res == False):
                self.log("robot gives %d clues and %d bombs"%(nb_clues_given,nb_bombs_given))
                return(choice)
            elif bomb_choice != None:
                self.log("robot chooses to save a bomb instead of other choice")
                return(bomb_choice)
            return (choice)

        if there_is_5:
            self.log("robot shows the 5")
            return("c5")



    def num_clue_score(self,hand,c):
        """Dans le cas d'un indice sur le numéro de c, retourne le nombre d'indices pertinents et le nombre de bombes créées"""
        game = self.game
        nb_clues = 0
        nb_bombs = 0
        already_given = []
        for ind_card in range(len(hand.cards)-1,-1,-1):
            card = hand.cards[ind_card]
       #     self.log(str(card))
         #  self.log(card.number,c.number,card.number_clue[0])
            if (card.number == c.number) & (not card.number_clue[0]):
        #        self.log(game.piles[card.color])
                if (game.piles[card.color] == (c.number-1)) & (nb_bombs == 0) & (card.color not in already_given):
                    nb_clues += 1
                    already_given.append(card.color)
                else:
                    if nb_clues == 0:
                        return(0,5)
                    nb_bombs += 1
        return(nb_clues,nb_bombs)

    def col_clue_score(self,hand,c): #les indices pertinents ne sont donc pas considérés comme des bombes en fait
        """Dans le cas d'un indice sur la couleur de c, retourne le nombre d'indices pertinents et le nombre de bombes créées"""
        game = self.game
        nb_clues = 0
        nb_bombs = 0
        ref_value = c.number
        for ind_card in range(len(hand.cards)-1,-1,-1):
            card = hand.cards[ind_card]
            if (card.color == c.color):
                if card.number == ref_value:
                    ref_value += 1
                    if nb_bombs == 0:
                        nb_clues += 1
                elif (not card.color_clue[0]) :
                    if nb_clues == 0:
                        return(0,5)
                    nb_bombs += 1
        return(nb_clues,nb_bombs)


    def give_discardable_clue(self):
        game = self.game
        for ind_hand in range(len(self.other_hands)-1,-1,-1):
            hand = self.other_hands[ind_hand]
            for ind_card in range(0,len(hand.cards)):
                card = hand.cards[ind_card]
                if card.number <= self.min_piles():
                    #self.log("cardnumb <= min pile",card)
                    return ("c%d"%(card.number))
                if card.color_clue[0]:
                    if game.piles[card.color] == 5:
                        #self.log("cardcolor is full",card)
                        return ("c%s"%(str(card.color)[0]))

    def give_punish_clue(self):
        """n'a pas été implémentée"""
        return()

    def give_random_clue(self):
        self.log("give a random clue")
        return("c%d"%(randint(1,5)))

    def discard_safely(self,hand):
        """Le robot défausse une carte qui n'est pas identifiée comme cruciale"""
        game = self.game
        for ind_card in range(0,len(hand.cards)):
            card = hand.cards[ind_card]
            if card.color_clue[0]:
                if game.piles[card.color] == 5:
                    return ("d%d"%(ind_card+1))
            if card.number_clue[0]:
                if card.number < self.min_piles():
                    return ("d%d"%(ind_card+1))        

    def discard_at_all_costs(self,hand):
        game = self.game
        for ind_card in range(0,len(hand.cards)): # FIX ME redondant ?
            card = hand.cards[ind_card]
            if card.color_clue[0]:
                if game.piles[card.color] == 5:
                    return ("d%d"%(ind_card+1))
            if card.number_clue[0]:
                if card.number < self.min_piles():
                    return ("d%d"%(ind_card+1))
        for ind_card in range(0,len(hand.cards)):
            card = hand.cards[ind_card]
            if (not card.color_clue[0]) & (not card.number_clue[0]) & (not card.crucial):
              return("d%d"%(ind_card+1))
        return("d1")

    def situation_is_risky(self):
        """Evalue si une carte cruciale risque d'être défaussée par le partenaire au prochain tour. Retourne son indice ou False"""
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
            risky = self.last_rep( hand.cards[ ind_chop_card ] )
            #self.log("la chop_card du partenaire est :",hand.cards[ind_chop_card],"est-ce une carte importante ? ",risky)
            if (risky):
                return(ind_chop_card)
            return(False)

    def last_rep(self,card):
        """Retourne un booleen indiquant si la carte est la dernière de sa nature dans la jeu"""
        game = self.game
        if card.number == 5:
            return(True)
        if card.number > 1:
            return(card in game.discard_pile.cards)
        if card.number == 1:
            return(game.discard_pile.cards.count(card) == 2)

    def conflit(self,hand,ind_card,c):
        """Utile avant de donner un indice. Retourne un booleen indiquant si dans le reste de la main (à gauche de la carte), il y a une carte possédant la couleur ou le chiffre de l'indice c"""
        game = self.game
        for i in range(ind_card + 1, len(hand.cards)):
            #self.log(str(hand.cards[i].number) == c,str(hand.cards[i].color)[0] == c)
            if (str(hand.cards[i].number) == c) or (str(hand.cards[i].color)[0] == c):
                return True
        return False

    def min_piles(self):
        """Indique le minimum des numéros de la configuration actuelle des piles"""
        game = self.game
        min = None
        for color in list(Color):
            if (min is None) or (game.piles[color] < min):
                min = game.piles[color]
        return(min)

    def max_piles(self): # not used so far
        """Indique le maximum des numéros de la configuration actuelle des piles"""
        game = self.game
        max = None
        for color in list(Color):
            if (max is None) or (game.piles[color] > max):
                max = game.piles[color]
        return(max)

    def possibly_playable(self,value): # et si c'est une couleur qui n'est pas jouable ? Ca traite seulement le numéro
        """Retourne un booleen indiquant si le numéro indiqué est peut-être jouable compte-tenu de la progression des piles"""
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
