import hanabi
from ai_almost_human_lvl4 import Robot_4

#python3 setup.py install --user
#cd ..\src & python3 setup.py install --user & cd ..\test	

#from hanabi import my_new_smart_ai


game = hanabi.Game(2)  # 2 players
#game.quiet = True
ai = Robot_4(game)
#ai.quiet = True

# pour jouer toute une partie
game.ai = ai
game.run()
