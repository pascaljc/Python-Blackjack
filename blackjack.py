import random

class Player():
	#this creates a player object. Suitable for player & dealer.
	def __init__(self,cash=0,name='',hand=[],bet=0,blackjack=False):
		self.cash=0
		self.name=''
		self.hand=[]
		self.bet=0
		self.blackjack=False		
class Card():
	def __init__(self):
		self.suit=''
		self.rank=''
		self.value_hard=0
		self.value_soft=0
	def getCard(self):
		return self.rank+" of "+self.suit
class Deck():
	def __init__(self):
		self.stack=[]
		self.created_size=0
		self.standard_size=52
	def size(self):
		return len(self.stack)
#some so-called 'global' objects to track.
player = Player()
player_split = Player()
dealer = Player(name="Dealer")
deck = Deck()
dealprog=0
	
def setup():
	global player, deck
	
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
	
	main()
	
def newdeck(n=1):

	suits = ['Diamonds','Hearts','Spades','Clubs']
	ranks = ['Ace','King','Queen','Jack','10','9','8','7','6','5','4','3','2']
	hard_values=[11,10,10,10,10,9,8,7,6,5,4,3,2]
	soft_values=[1,10,10,10,10,9,8,7,6,5,4,3,2]
	
	std_deck = Deck()
	finaldeck = Deck()
	
	card_data=zip(ranks,hard_values,soft_values)

	for i in suits:
		for j in card_data:
				newCard = Card()
				newCard.suit = i
				newCard.rank = j[0]
				newCard.value_hard = j[1]
				newCard.value_soft = j[2]
				std_deck.stack.append(newCard)
	
	std_deck.size=len(std_deck.stack)
	
	finaldeck.stack = std_deck.stack*n
	finaldeck.created_size = len(finaldeck.stack)
	random.shuffle(finaldeck.stack)
	#print finaldeck.size(), finaldeck.created_size, finaldeck.standard_size    #a little debugging
	return finaldeck
	
def deal(player_obj,number_of_players):
	global deck, dealprog
	
	#print deck.size(), deck.created_size, deck.standard_size    #a little debugging
	
	#first: Check if there are enough cards to go around
	if deck.size() < 26: #not happy about this arbitrary integer.
		print "Deck needs to be reshuffled"
		deck = newdeck(deck.created_size/deck.standard_size)
		
	i=0
	if dealprog == 0:
		while i < 2:
			player_obj.hand.append(deck.stack.pop(i))
			i+=(number_of_players)-1
		dealprog += 1
	else:
		while i < 2:
			player_obj.hand.append(deck.stack.pop(0))
			i+=1
			
	if value(player_obj.hand)==21 and len(player_obj.hand)<3:
		player_obj.blackjack = True

def hit(cards):
	global deck
	cards.append(deck.stack.pop(0))
	print "Hit results in ",cards[-1].getCard()
		
def doubledown():
	global deck, player
	hit(player.hand)
	print "Your cards are:"
	for item in player.hand:
		print item.getCard()
	print "The value is now",value(player.hand)
	if value(player.hand) > 21:
		print "You busted! You lose."
		print "You lost $",player.bet
		print "You now have $",player.cash
		playagain()
	else: stand()
	
def surrender():
	print "You have surrendered."
	player.cash += player.bet/2
	print "You sacrificed $",player.bet/2,"to withdraw."
	playagain()
	
def stand():
	global deck, player, dealer, dealerprog
	def win(con=''):
		if con == 'bust':
			print "Dealer busts! You win!!!"
			print "You win $",player.bet
			player.cash += 2*player.bet
		elif con == 'BJ':
			print "You won with a blackjack! Blackjack pays 3:2"
			print "You win $",(3./2)*player.bet
			player.cash += (5./2)*player.bet
		else:
			print "You won!"
			print "You win $",player.bet
			player.cash += 2*player.bet
	def lose():
		print "You lost!"
	def push():
		print "Push!"
		player.cash += player.bet
	
	print "The dealer reveals his other card:"
	print dealer.hand[0].getCard()
	print "The value of his hand is ",value(dealer.hand)
	if dealer.blackjack == True:
		print "Dealer has Blackjack! Uh-oh..."
	
	while value(dealer.hand) < 17:
		print "The dealer hits until he is at or equal to 17."
		hit(dealer.hand)
		print "Dealer is at ",value(dealer.hand)
	
	#cases
	
	#dealer busts
	if value(dealer.hand) > 21:
		win('bust')

	#the rest of the cases
	elif dealer.blackjack:
		if player.blackjack: 
			push()
		else: lose()  #dealer BJ trumps anything but BJ
	else:
		if player.blackjack: #check trump condition
			win('BJ') #special win condition, 3:2 for BJ
		elif value(player.hand) > value(dealer.hand): #player has higher val
			win()
		elif value(player.hand) < value(dealer.hand): #player has lower val
			lose()
		else: push() #true tie
	playagain()
			
def stand_split():
	return 0
			
def split():
	#splits hand, hits both new hands, then some stuff happens.... we will see
	global deck, player, player_split, dealer
	#need to split that hand
	player_split.hand.append(player.hand.pop(-1))
	hit(player.hand)
	hit(player_split.hand)
	
	#hands now played out one at a time
	#code MOL copied from Main.
	
	#Hand 1 GO!
	
	while decision == 0:	
		if len(player.hand)==2:
			firstpass = True
			
		if firstpass:
			print "Press 1 to hit, 2 to stand, 3 to double down, 4 to surrender."
			decision = intInput('z',input_message="Please enter 1 thru 4: ")
			if decision > 4:
				print "1 thru 4 only."
		else:
			while not firstpass:
				print "Press 1 to hit, 2 to stand"
				decision = intInput('z',input_message="Please enter 1 or 2: ")
				if decision > 2:
					print "1 or 2 only."
					
		##work it brother
		if decision == 1:
			hit(player.hand)
			print "Your cards are:"
			for item in player.hand:
				print item.getCard()
			print "Your hand value is",value(player.hand)
			if value(player.hand) == 21:
				print "You should stand."
				decision = 0
			elif value(player.hand)>21:
				print "You busted! You lose."
				print "You lost $",player.bet
				hand2()  #<-------- PAY ATTENTION HERE
			else: decision = 0
		elif decision == 2:
			print "Standing on hand 1..."
			hand2() #<-------- PAY ATTENTION HERE
		elif decision == 3:
			if player.bet > player.cash-player.bet:
				print "You can't double down, you don't have enough money."
				decision = 0
			else: doubledown()  #<-------- PAY ATTENTION HERE
		elif decision == 4:
			yn = ''
			while yn == '':
				print """Surrender: Gives up a half bet & retires ("folds")"""
				print "Are you sure?"
				yn = raw_input()
				if yn == 'y':
					surrender()  #<-------- PAY ATTENTION HERE
				elif yn == 'n':
					decision = 0
				else: 
					print "Please input y or n only."
					yn=''
		else: 
			decision = 0					
					
	def hand2():
					
					
def main():
	global deck, player, dealer
	if player.cash <= 0:
		print "You are BROKE! Get out!"
		return 0
	print "Please bet before the deal."
	while player.bet == 0.:
		player.bet = intInput(input_message="Enter your bet: $")
		if player.bet > player.cash:
			print "You bet too much, can't bet more than you have."
			player.bet = 0
			
	player.cash -= player.bet
	print "You now have $",player.cash
	
	deal(player,2)
	deal(dealer,2)

	print "Your cards are:"
	for item in player.hand:
		print item.getCard()
	print "Your hand value is",value(player.hand)

	print "The Dealer shows",dealer.hand[1].getCard()
	decision = 0
	

	while decision == 0:
		##check for split	
		if player.hand[0].rank == player.hand[1].rank:
			split = True
		else: split = False
		## check for 1st time
		if len(player.hand)==2:
			firstpass = True
		
		if split == True:
			print "Press 1 to hit, 2 to stand, 3 to double down, 4 to surrender, 5 to split."
			decision = intInput('z',input_message="Please enter 1 thru 5: ")
			if decision > 5:
				print "1 thru 5 only."
		elif firstpass == True:
				print "Press 1 to hit, 2 to stand, 3 to double down, 4 to surrender."
				decision = intInput('z',input_message="Please enter 1 thru 4: ")
				if decision > 4:
					print "1 thru 4 only."
		else:
			while firstpass == False:
				print "Press 1 to hit, 2 to stand"
				decision = intInput('z',input_message="Please enter 1 or 2: ")
				if decision > 2:
					print "1 or 2 only."
	
		##work it brother
		if decision == 1:
			hit(player.hand)
			print "Your cards are:"
			for item in player.hand:
				print item.getCard()
			print "Your hand value is",value(player.hand)
			if value(player.hand) == 21:
				print "You should stand."
				decision = 0
			elif value(player.hand)>21:
				print "You busted! You lose."
				print "You lost $",player.bet
				playagain()
			else: decision = 0
		elif decision == 2:
			stand()
		elif decision == 3:
			if player.bet > player.cash-player.bet:
				print "You can't double down, you don't have enough money."
				decision = 0
			else: doubledown()
		elif decision == 4:
			yn = ''
			while yn == '':
				print """Surrender: Gives up a half bet & retires ("folds")"""
				print "Are you sure?"
				yn = raw_input()
				if yn == 'y':
					surrender()
				elif yn == 'n':
					decision = 0
				else: 
					print "Please input y or n only."
					yn=''
		elif decision == 5 and split == True:
			yn = ''
			while yn == '':
				print """Split: Doubles bet, you will play two effective 'hands'."""
				print "Are you sure?"
				yn = raw_input()
				if yn == 'y':
					split()
				elif yn == 'n':
					decision = 0
				else: 
					print "Please input y or n only."
					yn=''

		else: 
			decision = 0
	
def playagain():
	global player, dealer, dealprog
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
			main()
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
		total = 0
		for item in cards:
			#print item.suit, item.rank, item.value_hard, item.value_soft
			total += item.value_hard
		return total

	def softTotal(cards):
		total = 0
		for card in cards:
			total += card.value_soft
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

"""-------------------------------------------------
TODO: GET SPLIT STANDING WORKING. POSSIBLE REWRITE OF STAND.
	- SHOULD STAND TAKE PLAYER OBJECTS AS ARGUMENTS? WHAT WOULD OUTPUTS BE
		IN THAT SCENARIO? SHOULD OUTPUTS CALL FUNCTIONS? OR JUST RETURN CONDITIONS?
	-OR SHOULD SPLIT_STAND BE A SEPERATE FUNCTION? 
	
	MAYBE STAND SHOULD TAKE TWO ARGUEMENTS... AND IF ONLY ONE PROVIDED, PROCEED NORMALLY, OTHERWISE
		DO THE SPLIT LOGIC
 	-SLEEP
 	"""