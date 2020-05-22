#IN104 groupe 5 : Alexis Fabrigoule et Grégoire Guillot

# Rapport de l'ai 

# Stratégie retenue

Pour programmer le robot, nous nous sommes interessés à une AI qui ne triche pas, et se rapproche le plus d'un raisonnement humain:
* Nous avons d'abord codé un premier robot de base qui s'appropriait le jeu hanabi et posait ses premières cartes sans tricher
* Ensuite, nous avons intégré les conventions "play right, discard left" pour un deuxième robot qui eut un taux de parties perdues très faible ( < 0,5 %) et un score moyen d'environ 14.
* Enfin, nous avons créé un troisième puis quatrième robot qui utilisent en plus la convention des "bombes" qui permet d'optimiser le score des parties gagnées.
* Notre objectif était de se concentrer sur imaginer un robot qui imitait au maximum un joueur humain, contre qui on pouvait jouer



# Robot 1

Le premier robot prend ses marques avec le module hanabi, 
- il peut intégrer les indices qu'on lui donne pour poser les premiers 1 des piles.
- il donne des indices sur les 1 du partenaire qui peuvent être joués

# Robot 2


# Robot 3

Le robot 3 et le robot 4 se rapprochent davantage encore d'un fonctionnement humain qui utilise les conventions les plus classiques :

- Ils défaussent à gauche et jouent à droite
- Les bombes : lorsqu'un indice est donné au robot, il reconnaît l'objectif qui était derrière en appliquant à une carte de son jeu un indice pertinent, qui lui indique qu'il peut la jouer. Les autres cartes concernées par l'indice sont répertoriées comme des "bombes", et seront prioritaires aux prochains tours lorsqu'il n'y a pas d'indices pertinents.

Les deux robots s'articulent autour de fonctions principales :

- La fonction play simule un joueur humain :
  - Détermine les cartes cruciales de son jeu avec set_crucial_card()
  - Le robot détermine si la situation est risquée avec situation_is_risky() : si le partenaire s'apprête à défausser une carte jugée cruciale. Si oui, il donne un indice pour l'empêcher de le faire.
  - De la même façon, si la prochaine carte bombe du partenaire n'est pas jouable, le robot la sauve
  - Il analyse ses indices et détermine ses cartes à indices pertinents et ses bombes.
  - S'il le peut, il joue une carte dont il est certain qu'elle est jouable (1 correct ou carte connue) ou qui possède un indice pertinent avec try_to_play_safely()
  - Sinon, il donne un indice jouable au joueur avec give_relevant_clue()
  - S'il ne peut pas, il joue une bombe s'il en a
  - Enfin, s'il n'en a pas, il défausse une carte avec discart_at_all_costs()


        def play(self):
                game = self.game
                self.log(game.examine_piles())
                have_clue = self.have_clue()
                self.set_crucial_cards() 
                risk = self.situation_is_risky()
                self.log("risk is",risk)
                self.log("Is the situation risky ? ",risk != False)
                if (risk != False) & (game.blue_coins > 0):
                    self.log("situation is risky")
                    ind_chop_card = risk
                    if not self.possibly_playable((self.other_hands[0].cards[0]).number): 
                        self.log("Robot saves playable chop card")
                        return("c%d"%(self.other_hands[0].cards[0]).number)
                    if self.give_playable_clue() != None:
                        self.log("Robot gives a playable clue")
                        return(self.give_playable_clue())
                    if self.give_discardable_clue() != None:
                        self.log("Robot gives a discardable clue")
                        return(self.give_discardable_clue())

                self.log("Robot possède des indices ? ",have_clue)
                if have_clue:
                    temp = self.try_to_play_card_safely()
                    self.log("play_safely = ",temp)
                    if temp != None:
                        self.log("Robot plays safely")
                        return(temp)
                if game.blue_coins > 0:
                    temp = self.give_playable_clue()
                    if temp != None:
                        self.log("Robot gives a playable clue or save a bomb")
                        return(temp)

                temp = self.try_to_play_a_bomb()
                if temp != None:
                    self.log("Robot tries to play a bomb")
                    return(temp)

                if game.blue_coins == 8:
                    temp = self.give_discardable_clue()
                    if temp != None:
                        self.log("Robot gives a discardable clue")
                        return(temp)
                    self.log("Robot gives a random clue") # FIX ME réfléchir à une optimisation
                    return(self.give_random_clue())
                self.log("Robot should discard")
                return(self.discard_at_all_costs(game.current_hand))

- La fonction have_clue() détermine les indices pertinents à sa disposition et les bombes de son jeu
  -  Elle analyse les indices de ses cartes et qualifie un indice de pertinent s'il vient d'être donné et si c'est le premier en partant de la droite.
  - Les indices 5 et les cartes entièrement connues, cas particuliers, sont aussi traités comme pertinents.
  - Les autres sont considérés comme des bombes.
  

        def have_clue(self):
                """Retourne un booleen indiquant si le robot a des indices, et détermine les bombes de son jeu en les analysant"""
                game = self.game
                res = False
                clue_is_bomb = False #permet de savoir quel indice est pertinent
                for ind_card in range(len(game.current_hand.cards)-1,-1,-1):
                    card = game.current_hand.cards[ind_card]
                    if card.color_clue[0]:
                        res = True
                        card.color_clue[1] += 1
                        if card.color_clue[1] == 1:
                            if clue_is_bomb & (not card.number_clue[0]):
                                card.bomb = True
                            clue_is_bomb = True
                        if card.number_clue[0]:
                            card.bomb = False
                    if card.number_clue[0]:
                        res = True
                        card.number_clue[1] += 1
                        if card.number_clue[1] == 1:
                            if clue_is_bomb & (not card.color_clue[0]):
                                self.log(card,"is spotted as a bomb")
                                card.bomb = True
                            clue_is_bomb = True
                        if card.color_clue[0]:
                            card.bomb = False
                return(res)

- La fonction give_relevant_clue() donne un indice jouable pour le partenaire en parcourant ses cartes de droite à gauche. Elle retient progressivement un indice, qu'elle modifie si elle en trouve un meilleur :
  - Si la carte est jouable et n'est pas une bombe, la fonction considère les indices de numéro ou de couleur qu'elle pourrait lui donner et les compare avec l'indice précédemment retenu en terme d'optimisation. Pour comparer le nombre de bombes créées si elle donne l'indice, la fonction fait appel à col_clue_score() et num_clue_score() qui retournent le nombre d'indices pertinents et de bombes engendrés.
  - Si la carte est la prochaine bombe du partenaire et qu'elle n'est pas jouable, la fonction retourne un indice pour la sauver
  - Si la fonction ne trouve pas d'indice jouable, elle ne renvoit rien
  
        def give_playable_clue(self): #FIX ME give 5 clue even if chop_card is playable
                """Donne un indice au partenaire"""
                game = self.game
                choice = None
                bomb_choice = None
                bomb_card = None
                there_is_5 = False
                (nb_clues_given,nb_bombs_given) = (0,5)


                other_first_bomb = None
                indic = None                                       
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
                            if (not card.color_clue[0]) & (not self.conflit(hand,ind_card,str(card.color)[0])):
                                (nb_clues,nb_bombs) = self.col_clue_score(hand,card)
                                if ( (nb_bombs < nb_bombs_given) & (nb_clues > 0) ) or ( (nb_bombs == nb_bombs_given) & (nb_clues > nb_clues_given) ):
                                    (nb_clues_given,nb_bombs_given) = (nb_clues,nb_bombs)
                                    choice = ("c%c"%(str(card.color)[0]))
                            if (not card.number_clue[0]) & (not self.conflit(hand,ind_card,card.number)):
                                (nb_clues,nb_bombs) = self.num_clue_score(hand,card)
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
                        if (card.number == 5) & (not card.number_clue[0]) & (not self.possibly_playable(5)) & (choice is None): #FIX ME le choix c5 devrait se faire en dehors de la boucle pour juger correctement
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
                    
                    
 
-

