import hanabi
from ai_almost_human_lvl1 import Robot_1

#python3 setup.py install --user
#cd ..\src & python3 setup.py install --user & cd ..\test	

#from hanabi import my_new_smart_ai
N=200
scores=[]
S=0

for i in range(0,N):
	game = hanabi.Game(2)  # 2 players
	game.quiet = True
	ai = Robot_1(game)
	ai.quiet = True
	#ai = my_new_smart_ai.RandomAI(game)

	# pour jouer toute une partie
	game.ai = ai
	game.run()

	scores.append(game.score)
	S += game.score
print(S/N)