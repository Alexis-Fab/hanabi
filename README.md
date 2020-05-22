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

''' def play(self):
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
        return(self.discard_at_all_costs(game.current_hand))'''



- add AIs. Some suggestions:
  - RandomAI (plays randomly),
  - DirectAI (plays whatever is hinted),
  - BGAAI (plays Board Game Arena's standard),
  - HansimAI (see below),
  - train a machine learning (I'm not sure if this will give anything interesting without powerful CPU/GPU resources),
  - design your own, from scratch or by improving an existing one.

Keep track of scores for all these games/AI. 
We will want to compare: different AIs on a same deck, or a given AI over a 1000 decks. 
We will need to see why a certain AI fails on a certain game.


- make it workable for up to 5 players.

- make it workable from two separate screens (network?)

- you may also design a GUI, but be warned that this is a very time-consuming task.
I like PySide2. Tkinter is more portable but harder to learn imho. 


During the project:
  - make sure you understand the "replay" mode
  - add tests (UnitTest or whole tests)
  - keep notes on your questions, decisions, discussions (github's wiki)




## Installation


    git clone https://github.com/JDGaraudEnsta/hanabi
    cd hanabi
    make        # pip installs it in the default directory ~/.local
    hanabi
    # and now you may play


If `hanabi` doesn't start (`bash: hanabi: command not found`), add this to your `~/.bashrc`:

    export PATH=$HOME/.local/bin:$PATH


## Bibliography

### Other Hanabi projects

* [A C++ bot: some strategies and success rates](https://github.com/Quuxplusone/Hanabi)
* [HanSim: the Hat guessing strategy](https://d0474d97-a-62cb3a1a-s-sites.googlegroups.com/site/rmgpgrwc/research-papers/Hanabi_final.pdf?attachauth=ANoY7cp_mjjD7lCb5HFxBphRWpSkE8SabM7PiOVWFwcNKSnpxENRLwTsQEgDMC6PIHuBmzP4oixvH_B8PZQmrHDyfA-ZLSKWb-Lx1WJNIUKUoxV1w0K0bWXelLPCi5MbXaByoVcukH4CEg-5N_iJP7mKSDHiV5ImwGDBCwQoT4mwvppVyA0BVb2Lhr-mGYFtUw3uBlds77azk5RjFZHGvAtvx6idYLvunLLj6BStHWHrNovX8p5KGFk%3D&attredirects=0)
* [HanSim: source code](https://github.com/rjtobin/HanSim)
* [boardgame arena](https://fr.boardgamearena.com/#!gamepanel?game=hanabi)
* [hanabi conventions (hanabi-live)](https://github.com/Zamiell/hanabi-conventions), and references therein.


### AI (deep learning)

* [deepmind: Atari](https://arxiv.org/pdf/1312.5602v1.pdf)
* [deepmind: SC2](https://arxiv.org/abs/1708.04782)
* [deepmind: Hanabi](https://arxiv.org/abs/1902.00506)
* [facebook's](https://ai.facebook.com/blog/building-ai-that-can-master-complex-cooperative-games-with-hidden-information/)


### Misc (coding principles, project, ...)

* [How to Write a Git Commit Message](https://chris.beams.io/posts/git-commit/)
* [keep it simple](https://en.wikipedia.org/wiki/KISS_principle)
* [rule of least surprise](http://www.catb.org/esr/writings/taoup/), [catbaz](http://www.catb.org/esr/writings/cathedral-bazaar/)
* [rubber duck debugging](https://en.wikipedia.org/wiki/Rubber_duck_debugging)
* [markdown (overview)](https://guides.github.com/features/mastering-markdown/), [markdown (in details)](https://github.github.com/gfm/)
* [BGA state machine](https://www.slideshare.net/boardgamearena/bga-studio-focus-on-bga-game-state-machine)
* dive into python3, esp. chapter on Unit testing
