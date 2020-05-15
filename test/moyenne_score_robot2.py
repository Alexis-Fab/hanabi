import hanabi
from ai_almost_human_lvl2 import Robot_2

#python3 setup.py install --user
#cd ..\src & python3 setup.py install --user & cd ..\test	

#from hanabi import my_new_smart_ai
N=50
scores=[]
S=0
failures = 0

for i in range(0,N):
	game = hanabi.Game(2)  # 2 players
	game.quiet = True
	ai = Robot_2(game)
	ai.quiet = True
	#ai = my_new_smart_ai.RandomAI(game)

	# pour jouer toute une partie
	game.ai = ai
	game.run()

	scores.append(game.score)
	if game.score == 0:
		failures += 1
	S += game.score
print(S/N)
print("failures : ",failures)