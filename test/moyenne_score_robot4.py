import hanabi
from ai_almost_human_lvl4 import Robot_4

#python3 setup.py install --user
#cd ..\src & python3 setup.py install --user & cd ..\test	

#from hanabi import my_new_smart_ai
N=1000
scores=[]
nb_win = 0
S=0
failures = 0

for i in range(0,N):
	game = hanabi.Game(2)  # 2 players
	game.quiet = True
	ai = Robot_4(game)
	ai.quiet = True
	#ai = my_new_smart_ai.RandomAI(game)

	# pour jouer toute une partie
	game.ai = ai
	game.run()

	scores.append(game.score)
	if game.score == 0:
		failures += 1
	else:
		nb_win += 1
	S += game.score
print("average score:",S/N)
print("failures : ",(failures/N)*100,"%")
print("average winning score:",S/nb_win)
