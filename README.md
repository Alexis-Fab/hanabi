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


