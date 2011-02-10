import random
from string import maketrans 

class Player():
	#this creates a player object. Suitable for player & dealer.
	def __init__(self,cash=0,name='',hand=[],bet=0,blackjack=False):
		self.cash=0
		self.name=''
		self.hand=[]
		self.bet=0
		self.blackjack=False

#some global objects to track.
player = Player()
dealer = Player(name="Dealer")
dealprog=0

def setup():
	#sets up the game. Player name, deck number, and starting funds are specified here
	print "Welcome to Python Blackjack."
	print "Please input your name:"
	player.name = raw_input()
	
	#decks
	print "Thanks,",player.name
	print "Please indicate the number of decks you would like to use in play."
	deck_num = intInput()
	deck = newdeck(deck_num)

	#starting funds
	print "Please indicate the level of starting funds you would like to play with." 
	player.cash = intInput(input_message="Enter a whole number): $")
	print "You will have $",player.cash,"to begin. Good luck!"
	
	main(deck)
	
def newdeck(n):
	"""This function creates decks, using n standard card decks, shuffled for play. Effectively 
	creates item 'deck' which is a list containing tuples of (value, suit)"""

	suits = ['D','H','S','C']
	ranks = ['A','K','Q','J','10','9','8','7','6','5','4','3','2']
	
	std_deck=[]
	for i in suits:
		for j in ranks:
			std_deck.append((j,i))
	
	deck=[]
	i=0
	
	while i < n:
		for j in range(len(std_deck)):
			deck.append(std_deck[j])
		i+=1
	
	random.shuffle(deck)
	return deck

def deal(deck,player_obj,number_of_players):
	"""Deals cards to player"""
	#first: Check if there are enough cards to go around
	print len(deck)
	if len(deck) < 20: #not happy about this arbitrary integer. Think i can fix with a deck class.
		print "Deck needs to be reshuffled"
		deck=newdeck(1)
	
	global dealprog
	i=0
	if dealprog == 0:
		while i < 2:
			player_obj.hand.append(deck.pop(i))
			i+=(number_of_players)-1
		dealprog += 1
	else:
		while i < 2:
			player_obj.hand.append(deck.pop(0))
			i+=1
			
	if value(player_obj.hand)==21 and len(player_obj.hand)<3:
		player_obj.blackjack = True

def hit(deck,cards):
	global deckprog
	print deck
	cards.append(deck.pop(0))
	print "Hit results in",cards[-1]
	return cards
		
def doubledown(deck):
	hit(deck,player.hand)
	print "Your hand is now",player.hand
	print "The value is now",value(player.hand)
	if value(player.hand) > 21:
		print "You busted! You lose."
		print "You lost $",player.bet
		print "You now have $",player.cash
		playagain(deck)
	else: stand(deck)

def stand(deck):
	def win(con=''):
		if con == 'bust':
			print "Dealer busts! You win!!!"
			print "You win $",player.bet
			player.cash += 2*player.bet
			playagain(deck)
		elif con == 'BJ':
			print "You won with a blackjack! Blackjack pays 3:2"
			print "You win $",(3./2)*player.bet
			player.cash += (5./2)*player.bet
			playagain(deck)
		else:
			print "You won!"
			print "You win $",player.bet
			player.cash += 2*player.bet
			playagain(deck)			
	def lose():
		print "You lost!"
		playagain(deck)
	def push():
		print "Push!"
		player.cash += player.bet
		playagain(deck)
	
	print "The dealer reveals his other card:"
	print dealer.hand
	print "The value of his hand is ",value(dealer.hand)
	if dealer.blackjack == True:
		print "Dealer has Blackjack! Uh-oh..."
	
	while value(dealer.hand) < 17:
		print "The dealer hits until he is at or equal to 17."
		hit(deck,dealer.hand)
		print "Dealer is at ",value(dealer.hand)
	
	#cases
	
	#dealer busts
	if value(dealer.hand) > 21:
		win('bust')

	#the rest of the cases
	elif dealer.blackjack == True:
		if player.blackjack == False: #dealer BJ trumps anything but BJ
			lose()
		elif player.blackjack == True:
			push()
	elif dealer.blackjack == False:
		if player.blackjack == True: #check trump condition
			win('BJ') #special win condition, 3:2 for BJ
		elif value(player.hand) > value(dealer.hand): #player has higher val
			win()
		elif value(player.hand) < value(dealer.hand): #player has lower val
			lose()
		elif value(player.hand) == value(dealer.hand): #true tie
			push()
	
def main(deck_object):
	if player.cash <= 0:
		print "You are BROKE! Get out!"
		return 0
	deck = deck_object
	print "Please bet before the deal."
	while player.bet == 0:
		player.bet = intInput('z',"Enter your bet: $")
		if player.bet > player.cash:
			print "You bet too much, can't bet more than you have."
			player.bet = 0
			
	player.cash -= player.bet
	print "You now have $",player.cash
	
	deal(deck,player,2)
	deal(deck,dealer,2)
	
	print "Your cards are",player.hand
	print "Your hand value is",value(player.hand)

	print "The Dealer shows",dealer.hand[:1]
	decision = 0
	
	##check for split	
	while decision == 0:
		if player.hand[0][0] == player.hand[1][0]:
			split = True
		else: split = False
		
		while split == True:
			print "Press 1 to hit, 2 to stand, 3 to double down, 4 to surrender, 5 to split."
			decision = intInput('z',input_message="Please enter 1 thru 5: ")
			if decision > 5:
				print "1 thru 5 only."
		else: 
			print "Press 1 to hit, 2 to stand, 3 to double down, 4 to surrender."
			decision = intInput('z',input_message="Please enter 1 thru 4: ")
			if decision > 4:
				print "1 thru 4 only."
	
		##work it brother
		if decision == 1:
			hit(deck,player.hand)
			print "Your cards are",player.hand
			print "Your hand value is",value(player.hand)
			if value(player.hand) == 21:
				print "You should stand."
				decision = 0
			elif value(player.hand)>21:
				print "You busted! You lose."
				print "You lost $",player.bet
				playagain(deck)
			else: decision = 0
		elif decision == 2:
			stand(deck)
		elif decision == 3:
			if player.bet > player.cash-player.bet:
				print "You can't double down, you don't have enough money."
				decision = 0
			else: doubledown(deck)
		elif decision == 4:
			print 4
		elif decision == 5 and split == True:
			print 5
		else: 
			decision = 0
	
def playagain(deck):
	global dealprog
	yn = ''
	while yn == '':
		print "You have $",player.cash,"available to bet with."
		print "Would you like to play again? (y/n)"
		yn = raw_input()
		if yn == 'y':
			#reset everything
			dealprog = 0
			player.bet=0
			player.hand=[]
			dealer.hand=[]
			dealer.blackjack=False
			player.blackjack=False
			#go back
			main(deck)
		elif yn == 'n':
			print "Thank you for playing!"
			return 0
		else: 
			print "Please input y or n only."
			yn=''
	return 0
	
def intInput(n='',input_message="(Enter a whole number): ",error_message="Please use numbers only: "):
	import string
	n = raw_input(input_message)
	while n.isdigit() == False:
		n = raw_input(error_message)
	return int(n)

def value(cards):

	#What about 3 or more aces?
	
	def hardTotal(cards):
		ranks = ['A','K','Q','J','10','9','8','7','6','5','4','3','2']
		values= ['11','10','10','10','10','9','8','7','6','5','4','3','2']
		rank_to_val = zip(ranks,values)
		total=0
		for item in cards:
			for value in rank_to_val:
				if item[0] == value[0]:
					total = total + int(value[1])
		return total

	def softTotal(cards):
		ranks = ['A','K','Q','J','10','9','8','7','6','5','4','3','2']
		values= ['1','10','10','10','10','9','8','7','6','5','4','3','2']
		rank_to_val = zip(ranks,values)
		total=0
		for item in cards:
			for value in rank_to_val:
				if item[0] == value[0]:
					total = total + int(value[1])
		return total

	if hardTotal(cards)==softTotal(cards):
		return hardTotal(cards)
	elif hardTotal(cards)>softTotal(cards):
		if hardTotal(cards)-20 == softTotal(cards):
			#this is the 2 ace case, this is cheating I think.
			if softTotal(cards)+10 > 21:
				return softTotal(cards)
			else: return softTotal(cards) + 10
		elif hardTotal(cards)>21:
			return softTotal(cards)
		else: return hardTotal(cards)

setup()

