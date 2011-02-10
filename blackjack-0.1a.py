import random
from string import maketrans 

deckprog = 0

def newdeck(n):
	"""This function creates decks, using n standard card decks, shuffled for play. Effectively 
	creates item 'deck' which is a list containing tuples of (value, suit)"""

	suits = ['D','C','S','H']
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

def deal(deck,player):
	global deckprog
	"""Deals 2 cards to player & dealer each, starting with player and going in sequence"""
	player_cards=[]
	i=0
	while i < 3:
		if player=='user':
			player_cards.append(deck[i])
			deckprog+=1
		elif player=='dealer':
			player_cards.append(deck[i+1])
			deckprog+=1
		i+=2
	
	return(player_cards)

def hit(deck,cards):
	global deckprog
	cards.append(deck[deckprog])
	print "Hit results in",deck[deckprog]
	deckprog+=1
	return cards

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
		
def doubledown(deck,cards,dealer,player):
	hit(deck,cards)
	print "Your hand is now",cards
	print "The value is now",value(cards)
	if value(ncards) > 21:
		print "You busted! You lose."
		playagain()
	else: stand(deck,dealer,player)

def stand(deck,dealer,player):
	print "The dealer reveals his other card:"
	print dealer
	print "The value of his hand is at",value(dealer)
	
	while value(dealer) < 17:
		print "The dealer hits until he is at or equal to 17."
		hit(deck,dealer)
		print "Dealer is at ",value(dealer)
	
	if value(dealer) > 21:
		print "Dealer busts! You win!!!"
	
	elif value(dealer) < value(player):
		print "You win!!!"
		
	elif value(dealer)>=value(player):
		print "Oh Noes! The Dealer beat you! hahahaha"
		
	playagain()
	
def playagain():
	yn = ''
	while yn == '':
		print "Would you like to play again? (y/n)"
		yn = raw_input()
		if yn == 'y':
			main()
		elif yn == 'n':
			print "Thank you for playing!"
			return 0
		else: 
			print "Please input y or n only."
			yn=''
	return 0
	
def main(deck,player_cash):
	print "Welcome to Python Blackjack."
	deck=newdeck(5)
	player_cards=deal(deck,'user')
	dealer_cards=deal(deck,'dealer')
	print "Your cards are",player_cards
	print "The value of your hand is",value(player_cards)
	print "The dealer shows",dealer_cards[:1]
	
	#time to talk
	action = 0
	while action==0:
		print "What do you do? Press 1 to hit, 2 to double down, 3 to stand"
		action=input()
		
		if action==1 and value(player_cards)==21:
			print 'ARE YOU SURE YOU WANT TO DO THAT???'
			action = 0
			
		elif action==1:
			hit(deck,player_cards)
			print "Your hand is now",cards
			print "The value of your hand is",value(cards)
			if value(player_cards) == 21:
				print "You should stand; Dealer must tie to push."
				action = 0
			elif value(player_cards)>21:
				print "You busted! You lose."
			else: action = 0
			
		elif action==2:
			print "Are you sure? This doubles the bet, but you must stand on the next card. (y/n)"
			yn = ''
			while yn == '':
				yn = raw_input()
				if yn == 'y':
					doubledown(deck,player_cards,dealer_cards,player_cards)
				elif yn == 'n':
					action = 0
				else: 
					print "Please input y or n only."
					yn=''
			
		elif action==3:
			print "The dealer tries to beat you..."
			stand(deck,dealer_cards,player_cards)

		else:
			print "please try again"
			action = 0
		
	return 0

main()

