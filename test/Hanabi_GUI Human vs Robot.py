#Hanabi GUI

import hanabi
from hanabi.deck import Color
from ai_almost_human_lvl4 import Robot_4

import tkinter as tk
from PIL import ImageTk, Image

images_dir = "C:\\Users\\Alexis\\hanabi\\GUI\\Images\\"

class GUI():

	def __init__(self):

		self.game=hanabi.Game(2)
		self.game.ai = Robot_4(self.game)
		self.game.ai.quiet = True

		#This creates the main window of an application
		window = tk.Tk()
		window.title=("Welcome to Hanabi")
		window.geometry("1850x1000")
		window.columnconfigure(50, minsize=640)
		for i in range(5,31):
			if i not in [9,14,19,24,29]:
				window.columnconfigure(i, minsize=30)
		window.rowconfigure(20, minsize=50)



		##Charge les images :
		def Resize_Image(image, maxsize):
		    r1 = image.size[0]/maxsize[0] # width ratio
		    r2 = image.size[1]/maxsize[1] # height ratio
		    ratio = max(r1, r2)
		    newsize = (int(image.size[0]/r1), int(image.size[1]/r2))
		    image = image.resize(newsize, Image.ANTIALIAS)
		    return image

		

		#define background :
		background_image = ImageTk.PhotoImage(Image.open(images_dir + "paper-background.jpg"))
		background_label = tk.Label(window, image=background_image)
		background_label.place(x=0, y=0, relwidth=1, relheight=1)


		self.dico_color = {"Blue" : "#0005a3", "Purple" : "#7a1594", "Green" : "green", "Yellow" : "#c99700", "Red" : "#a80a0a"}


		self.image_back = ImageTk.PhotoImage(Resize_Image(Image.open(images_dir + "back.png"), (170,230)))
		self.image_back_selected = ImageTk.PhotoImage(Resize_Image(Image.open(images_dir + "back_selected.png"), (170,230)))


		self.image_B1 = ImageTk.PhotoImage(Resize_Image(Image.open(images_dir + "B1.PNG"), (170,230)))
		self.image_B2 = ImageTk.PhotoImage(Resize_Image(Image.open(images_dir + "B2.PNG"), (170,230)))
		self.image_B3 = ImageTk.PhotoImage(Resize_Image(Image.open(images_dir + "B3.PNG"), (170,230)))
		self.image_B4 = ImageTk.PhotoImage(Resize_Image(Image.open(images_dir + "B4.PNG"), (170,230)))
		self.image_B5 = ImageTk.PhotoImage(Resize_Image(Image.open(images_dir + "B5.PNG"), (170,230)))

		self.image_R1 = ImageTk.PhotoImage(Resize_Image(Image.open(images_dir + "R1.PNG"), (170,230)))
		self.image_R2 = ImageTk.PhotoImage(Resize_Image(Image.open(images_dir + "R2.PNG"), (170,230)))
		self.image_R3 = ImageTk.PhotoImage(Resize_Image(Image.open(images_dir + "R3.PNG"), (170,230)))
		self.image_R4 = ImageTk.PhotoImage(Resize_Image(Image.open(images_dir + "R4.PNG"), (170,230)))
		self.image_R5 = ImageTk.PhotoImage(Resize_Image(Image.open(images_dir + "R5.PNG"), (170,230)))

		self.image_G1 = ImageTk.PhotoImage(Resize_Image(Image.open(images_dir + "G1.PNG"), (170,230)))
		self.image_G2 = ImageTk.PhotoImage(Resize_Image(Image.open(images_dir + "G2.PNG"), (170,230)))
		self.image_G3 = ImageTk.PhotoImage(Resize_Image(Image.open(images_dir + "G3.PNG"), (170,230)))
		self.image_G4 = ImageTk.PhotoImage(Resize_Image(Image.open(images_dir + "G4.PNG"), (170,230)))
		self.image_G5 = ImageTk.PhotoImage(Resize_Image(Image.open(images_dir + "G5.PNG"), (170,230)))

		self.image_P1 = ImageTk.PhotoImage(Resize_Image(Image.open(images_dir + "P1.PNG"), (170,230)))
		self.image_P2 = ImageTk.PhotoImage(Resize_Image(Image.open(images_dir + "P2.PNG"), (170,230)))
		self.image_P3 = ImageTk.PhotoImage(Resize_Image(Image.open(images_dir + "P3.PNG"), (170,230)))
		self.image_P4 = ImageTk.PhotoImage(Resize_Image(Image.open(images_dir + "P4.PNG"), (170,230)))
		self.image_P5 = ImageTk.PhotoImage(Resize_Image(Image.open(images_dir + "P5.PNG"), (170,230)))

		self.image_Y1 = ImageTk.PhotoImage(Resize_Image(Image.open(images_dir + "Y1.PNG"), (170,230)))
		self.image_Y2 = ImageTk.PhotoImage(Resize_Image(Image.open(images_dir + "Y2.PNG"), (170,230)))
		self.image_Y3 = ImageTk.PhotoImage(Resize_Image(Image.open(images_dir + "Y3.PNG"), (170,230)))
		self.image_Y4 = ImageTk.PhotoImage(Resize_Image(Image.open(images_dir + "Y4.PNG"), (170,230)))
		self.image_Y5 = ImageTk.PhotoImage(Resize_Image(Image.open(images_dir + "Y5.PNG"), (170,230)))

		self.image_empty_B = ImageTk.PhotoImage(Resize_Image(Image.open(images_dir + "empty blue.jpg"), (180,70)))
		self.image_empty_R = ImageTk.PhotoImage(Resize_Image(Image.open(images_dir + "empty red.jpg"), (180,70)))
		self.image_empty_Y = ImageTk.PhotoImage(Resize_Image(Image.open(images_dir + "empty yellow.jpg"), (180,70)))
		self.image_empty_P = ImageTk.PhotoImage(Resize_Image(Image.open(images_dir + "empty purple.jpg"), (180,70)))
		self.image_empty_G = ImageTk.PhotoImage(Resize_Image(Image.open(images_dir + "empty green.jpg"), (180,70)))


		self.image_clue1 = ImageTk.PhotoImage(Resize_Image(Image.open(images_dir + "clue1.PNG"), (50,50)))
		self.image_clue2 = ImageTk.PhotoImage(Resize_Image(Image.open(images_dir + "clue2.PNG"), (50,50)))
		self.image_clue3 = ImageTk.PhotoImage(Resize_Image(Image.open(images_dir + "clue3.PNG"), (50,50)))
		self.image_clue4 = ImageTk.PhotoImage(Resize_Image(Image.open(images_dir + "clue4.PNG"), (50,50)))
		self.image_clue5 = ImageTk.PhotoImage(Resize_Image(Image.open(images_dir + "clue5.PNG"), (50,50)))

		self.image_clueB = ImageTk.PhotoImage(Resize_Image(Image.open(images_dir + "clueB.PNG"), (50,50)))
		self.image_clueR = ImageTk.PhotoImage(Resize_Image(Image.open(images_dir + "clueR.PNG"), (50,50)))
		self.image_clueY = ImageTk.PhotoImage(Resize_Image(Image.open(images_dir + "clueY.PNG"), (50,50)))
		self.image_clueP = ImageTk.PhotoImage(Resize_Image(Image.open(images_dir + "clueP.PNG"), (50,50)))
		self.image_clueG = ImageTk.PhotoImage(Resize_Image(Image.open(images_dir + "clueG.PNG"), (50,50)))



		self.dico_images = {"B1" : self.image_B1, "B2" : self.image_B2, "B3" : self.image_B3, "B4" : self.image_B4, "B5" : self.image_B5,
							"R1" : self.image_R1, "R2" : self.image_R2, "R3" : self.image_R3, "R4" : self.image_R4, "R5" : self.image_R5,
							"G1" : self.image_G1, "G2" : self.image_G2, "G3" : self.image_G3, "G4" : self.image_G4, "G5" : self.image_G5,
							"P1" : self.image_P1, "P2" : self.image_P2, "P3" : self.image_P3, "P4" : self.image_P4, "P5" : self.image_P5,
							"Y1" : self.image_Y1, "Y2" : self.image_Y2, "Y3" : self.image_Y3, "Y4" : self.image_Y4, "Y5" : self.image_Y5,

							"1" : self.image_clue1, "2" : self.image_clue2, "3" : self.image_clue3, "4" : self.image_clue4, "5" : self.image_clue5,
							"B" : self.image_clueB, "R" : self.image_clueR, "G" : self.image_clueG, "P" : self.image_clueP, "Y" : self.image_clueY }



		## Widgets :


		self.button_discard = tk.Button(window, text="Discard", padx=85, pady=10, command = lambda:self.card_discarded()) .grid(row=30,column=5, columnspan=15, sticky=tk.S)
		self.button_play = tk.Button(window, text="Play Card", padx=80, pady=10, command = lambda:self.card_played()) .grid(row=30,column=15, columnspan=15, sticky=tk.S)

		self.button_clue_number = tk.Button(window, width=33, height=2, fg="#ffcbb3", bg = "#db7337", font = ("Courier", 21))
		self.button_clue_color = tk.Button(window, width=35, height=2, fg="#ffcbb3", font = ("Courier", 20))



		#Main courante :

		tk.Label(window, text="Your Hand", fg= "#ffcbb3", bg = "#db7337", font = ("Courier", 16), width=9) .grid(row=30, column=5, columnspan=5, sticky=tk.SW)

		self.button_card_1 = tk.Button(window, image = self.image_back, borderwidth=10, command=lambda:self.card_selection(1))
		self.button_card_2 = tk.Button(window, borderwidth=10, image = self.image_back, command=lambda:self.card_selection(2))
		self.button_card_3 = tk.Button(window, borderwidth=10, image = self.image_back, command=lambda:self.card_selection(3))
		self.button_card_4 = tk.Button(window, borderwidth=10, image = self.image_back, command=lambda:self.card_selection(4))
		self.button_card_5 = tk.Button(window, borderwidth=10, image = self.image_back, command=lambda:self.card_selection(5))

		self.button_card_1.grid(row = 50,column=5, columnspan=5, sticky=tk.W)
		self.button_card_2.grid(row = 50,column=10, columnspan=5)
		self.button_card_3.grid(row = 50,column=15, columnspan=5)
		self.button_card_4.grid(row = 50,column=20, columnspan=5)
		self.button_card_5.grid(row = 50,column=25, columnspan=5)

		self.dico_buttons = {1 : self.button_card_1, 2 : self.button_card_2, 3 : self.button_card_3, 4 : self.button_card_4, 5 : self.button_card_5}


		self.button_card_1.selected = 0
		self.button_card_2.selected = 0
		self.button_card_3.selected = 0
		self.button_card_4.selected = 0
		self.button_card_5.selected = 0


		self.label_number_clue1 = tk.Label(window, borderwidth = 0)
		self.label_number_clue2 = tk.Label(window, borderwidth = 0)
		self.label_number_clue3 = tk.Label(window, borderwidth = 0)
		self.label_number_clue4 = tk.Label(window, borderwidth = 0)
		self.label_number_clue5 = tk.Label(window, borderwidth = 0)

		self.label_color_clue1 = tk.Label(window, borderwidth = 0)
		self.label_color_clue2 = tk.Label(window, borderwidth = 0)
		self.label_color_clue3 = tk.Label(window, borderwidth = 0)
		self.label_color_clue4 = tk.Label(window, borderwidth = 0)
		self.label_color_clue5 = tk.Label(window, borderwidth = 0)


		self.dico_clues = { 1 : [self.label_number_clue1, self.label_color_clue1],
							2 : [self.label_number_clue2, self.label_color_clue2],
							3 : [self.label_number_clue3, self.label_color_clue3],
							4 : [self.label_number_clue4, self.label_color_clue4],
							5 : [self.label_number_clue5, self.label_color_clue5] }


		#Main partenaire :

		tk.Label(window, text="Partner Hand", fg= "#ffcbb3", bg = "#db7337", font = ("Courier", 16), width=12) .grid(row=0, column=5, columnspan=5, sticky=tk.SW)

		self.button_partner_1 = tk.Button(window, image = self.image_back, borderwidth=10, command=lambda:self.partner_selection(1))
		self.button_partner_2 = tk.Button(window, borderwidth=10, image = self.image_back, command=lambda:self.partner_selection(2))
		self.button_partner_3 = tk.Button(window, borderwidth=10, image = self.image_back, command=lambda:self.partner_selection(3))
		self.button_partner_4 = tk.Button(window, borderwidth=10, image = self.image_back, command=lambda:self.partner_selection(4))
		self.button_partner_5 = tk.Button(window, borderwidth=10, image = self.image_back, command=lambda:self.partner_selection(5))

		self.button_partner_1.grid(row = 10, rowspan=10, column=5, columnspan=5)
		self.button_partner_2.grid(row = 10, rowspan=10, column=10, columnspan=5)
		self.button_partner_3.grid(row = 10, rowspan=10, column=15, columnspan=5)
		self.button_partner_4.grid(row = 10, rowspan=10, column=20, columnspan=5)
		self.button_partner_5.grid(row = 10, rowspan=10, column=25, columnspan=5)

		self.button_partner_1.selected = 0
		self.button_partner_2.selected = 0
		self.button_partner_3.selected = 0
		self.button_partner_4.selected = 0
		self.button_partner_5.selected = 0


		self.dico_partner_buttons = {1 : self.button_partner_1, 2 : self.button_partner_2, 3 : self.button_partner_3, 4 : self.button_partner_4, 5 : self.button_partner_5}


		self.label_number_partner_clue1 = tk.Label(window, borderwidth = 0)
		self.label_number_partner_clue2 = tk.Label(window, borderwidth = 0)
		self.label_number_partner_clue3 = tk.Label(window, borderwidth = 0)
		self.label_number_partner_clue4 = tk.Label(window, borderwidth = 0)
		self.label_number_partner_clue5 = tk.Label(window, borderwidth = 0)

		self.label_color_partner_clue1 = tk.Label(window, borderwidth = 0)
		self.label_color_partner_clue2 = tk.Label(window, borderwidth = 0)
		self.label_color_partner_clue3 = tk.Label(window, borderwidth = 0)
		self.label_color_partner_clue4 = tk.Label(window, borderwidth = 0)
		self.label_color_partner_clue5 = tk.Label(window, borderwidth = 0)


		self.dico_partner_clues = { 1 : [self.label_number_partner_clue1, self.label_color_partner_clue1],
									2 : [self.label_number_partner_clue2, self.label_color_partner_clue2],
									3 : [self.label_number_partner_clue3, self.label_color_partner_clue3],
									4 : [self.label_number_partner_clue4, self.label_color_partner_clue4],
									5 : [self.label_number_partner_clue5, self.label_color_partner_clue5] }


		#Piles

		self.label_pile_B = tk.Label(window, image=self.image_empty_B, anchor=tk.NW, height=60, width=175) 
		self.label_pile_G = tk.Label(window, image=self.image_empty_G, anchor=tk.NW, height=60, width=174)
		self.label_pile_R = tk.Label(window, image=self.image_empty_R, anchor=tk.NW, height=60, width=173)
		self.label_pile_Y = tk.Label(window, image=self.image_empty_Y, anchor=tk.NW, height=60, width=176)
		self.label_pile_P = tk.Label(window, image=self.image_empty_P, anchor=tk.NW, height=60, width=176)

		self.label_pile_B .grid(row=22, column = 100)
		self.label_pile_G .grid(row=24, column = 100)
		self.label_pile_R .grid(row=26, column = 100)
		self.label_pile_Y .grid(row=28, column = 100)
		self.label_pile_P .grid(row=30, column = 100)


		self.dico_piles = {'B' : self.label_pile_B, 'G' : self.label_pile_G, 'R' : self.label_pile_R, 'Y' : self.label_pile_Y, 'P' : self.label_pile_P}


		#Other

		self.myFriendlyLabel = tk.Label(window, fg = "#ffcbb3", bg = "#db7337", text = "...", font = ("Courier", 20), width = 40, height = 3)
		self.myFriendlyLabel.grid(row = 24, rowspan=10, column = 5, columnspan = 25, pady = (0,0))


		self.label_discard_pile = tk.Message(window, width = 750, bg="#db7337", fg="black", font=("Courier", 30), text="Discard Pile :", anchor=tk.NW, relief=tk.RIDGE)
		self.label_discard_pile.grid(row = 50, column=50, columnspan=100)


		self.selection = None
		self.not_finished = True
		

		tk.Label(window, text="Welcome ! Let's play Hanabi", fg="#ffcbb3", bg = "#d15e30", font="none 22 bold") .grid(row=0, column=5, columnspan=25, pady=(0,10))

		partner_hand = self.game.hands[1]
		for ind_card in range(len(partner_hand)):
			self.dico_partner_buttons[ind_card +1].configure(image = self.dico_images[str(partner_hand.cards[ind_card])])




		#Start the GUI
		window.mainloop()




	def new_turn(self):
		game=self.game
		if len(game.deck.cards) == 0:
			if not self.not_finished:
				self.end_game()
			elif self.not_finished is True:
				self.not_finished = 2
			else:
				self.not_finished -= 1
		if self.not_finished:
			game.turn(game.ai)
		if len(game.deck.cards) == 0:
			if not self.not_finished:
				self.end_game()
			elif self.not_finished is True:
				self.not_finished = 2
			else:
				self.not_finished -= 1
			self.myFriendlyLabel.configure(text="This is your last move")
		if self.not_finished:
			hand = game.current_hand
			partner_hand = game.hands[1]
			self.label_discard_pile.configure(text="Discard Pile :" + str(game.discard_pile))
			for ind_card in range(len(partner_hand)):
				self.dico_partner_buttons[ind_card +1].configure(image = self.dico_images[str(partner_hand.cards[ind_card])])
				card = partner_hand.cards[ind_card]
				if card.number_clue[0]:
					self.dico_partner_clues[ind_card+1][0].configure(image = self.dico_images[card.number_clue[0]])
					self.dico_partner_clues[ind_card+1][0].grid(row = 20, column = (1+ind_card)*5+2)
				else:
					self.dico_partner_clues[ind_card+1][0].grid_forget()
				if card.color_clue[0]:
					self.dico_partner_clues[ind_card+1][1].configure(image = self.dico_images[card.color_clue[0]])
					self.dico_partner_clues[ind_card+1][1].grid(row = 20, column = (1+ind_card)*5+3)
				else:
					self.dico_partner_clues[ind_card+1][1].grid_forget()

			for ind_card in range(len(hand)):
				card = hand.cards[ind_card]
				if card.number_clue[0]:
					self.dico_clues[ind_card+1][0].configure(image = self.dico_images[card.number_clue[0]])
					self.dico_clues[ind_card+1][0].grid(row = 60, column = (1+ind_card)*5+2)
				else:
					self.dico_clues[ind_card+1][0].grid_forget()
				if card.color_clue[0]:
					self.dico_clues[ind_card+1][1].configure(image = self.dico_images[card.color_clue[0]])
					self.dico_clues[ind_card+1][1].grid(row = 60, column = (1+ind_card)*5+3)
				else:
					self.dico_clues[ind_card+1][1].grid_forget()


			for color in list(Color):
				max_card = str(color)[0]+str(game.piles[color])
				if int(max_card[1]):
					self.dico_piles[max_card[0]].configure(image=self.dico_images[max_card])




	def card_played(self) :
		self.button_clue_number.grid_forget()
		self.button_clue_color.grid_forget()
		if self.selection == None :
			self.myFriendlyLabel.configure(text="Please select a card first !", fg="white", bg = "red")
		else :
			card = self.game.current_hand.cards[int(self.selection[-1]) - 1]
			if card.number == (self.game.piles[card.color]+1) :
				self.myFriendlyLabel.configure(fg="#ffcbb3", bg = "#db7337", text="Well played !")
			else:
				self.myFriendlyLabel.configure(fg="#ffcbb3", bg = "#db7337", text="Bad luck :/")
			self.game.turn("p" + self.selection[-1])
			self.dico_buttons[int(self.selection[-1])].configure(image = self.image_back)
			self.dico_buttons[int(self.selection[-1])].selected = 0
			self.selection = None
			self.new_turn()

	def card_discarded(self):
		self.button_clue_number.grid_forget()
		self.button_clue_color.grid_forget()
		if self.selection == None :
			self.myFriendlyLabel.configure(text="Please select a card first !", fg="white", bg = "red")
		elif self.game.blue_coins == 8:
			 self.myFriendlyLabel.configure(text="There are 8 clue coins, you can't discard", fg="white", bg = "red")
		else:
			card = self.game.current_hand.cards[int(self.selection[-1]) - 1]
			self.myFriendlyLabel.configure(fg="#ffcbb3", bg = "#db7337", text="You discard "+str(card))
			self.game.turn("d" + self.selection[-1])
			self.dico_buttons[int(self.selection[-1])].configure(image = self.image_back)
			self.dico_buttons[int(self.selection[-1])].selected = 0
			self.selection = None
			self.new_turn()



	def card_selection(self,ind) :
		self.button_clue_number.grid_forget()
		self.button_clue_color.grid_forget()
		button_card = self.dico_buttons[ind]
		button_card.selected = 1 - button_card.selected
		if button_card.selected :
			button_card.configure(image = self.image_back_selected)
			self.selection = "current " + str(ind)
			for i in self.dico_buttons :
				if i != ind :
					self.dico_buttons[i].selected = 0
					self.dico_buttons[i].configure(image = self.image_back)
			self.myFriendlyLabel.configure(fg="#ffcbb3", bg = "#db7337", text="Wanna play or discard this one ?")
		else :
			button_card.configure(image = self.image_back)
			self.selection = None
		if self.selection == None :
			self.myFriendlyLabel.configure(text="...", bg="#db7337", fg="#ffcbb3")

	def partner_selection(self,ind):
		self.myFriendlyLabel.configure(fg="#ffcbb3", bg = "#db7337", text="Wanna give a clue ?")
		if self.selection != None:
			self.dico_buttons[int(self.selection[-1])].configure(image = self.image_back)
			self.dico_buttons[int(self.selection[-1])].selected = 0
			self.selection = None

		self.button_clue_number.configure(text="Give the clue "+str(self.game.hands[1].cards[ind-1].number), command=lambda:self.give_clue(str(self.game.hands[1].cards[ind-1].number)))
		self.button_clue_color.configure(text="Give the clue "+str(self.game.hands[1].cards[ind-1].color), bg=self.dico_color[str(self.game.hands[1].cards[ind-1].color)], command=lambda:self.give_clue(str(self.game.hands[1].cards[ind-1].color)[0]))
		self.button_clue_number.grid(row = 10, column = 50, padx=(20,0))
		self.button_clue_color.grid(row = 15, column = 50, padx=(20,0))

	def give_clue(self,c):
		self.button_clue_number.grid_forget()
		self.button_clue_color.grid_forget()
		if self.game.blue_coins == 0:
			 self.myFriendlyLabel.configure(text="There is no more clue coin, you can't give a clue", fg="white", bg = "red")
		else:
			self.myFriendlyLabel.configure(fg="#ffcbb3", bg = "#db7337", text="You gave a clue") #FIX ME precise which clue
			self.game.turn("c" + c)
			self.new_turn()

	def end_game(self):
		self.myFriendlyLabel.configure(text="Game is over")






GUI()