# TODO incorporate ADVENTURE into explanation

# ************************************************************************
# The Game Recommender
# By Sam Levatich
# A CPSC 458 Final Project
# ************************************************************************

import operator
import sys

# ************************************************************************
# Global Variables
# ************************************************************************


users = {}
games = {}

GENRE_FACTOR = 1	# How much does genre similarity matter?
RATING_FACTOR = 1	# How much does average score matter?
ADVENTURE = 1		# How willing are we to embrace new genres?


# ************************************************************************
# OBJECTION! (Objects)
# ************************************************************************

# Holds all game info
class Game:
	def __init__(self,user,title,tags,score,time):
		self.user  = user
		self.title = title
		self.tags  = tags
		self.score = score
		self.time  = time

	def __repr__(self):
		return repr((self.user, self.title, self.tags, self.score, self.time))

# Represents one game by the users (review) associated with it
class GameList:
	def __init__(self,name):
		self.name  = name
		self.games = []

	def __repr__(self):
		return repr(self.games)

	# Update uses this function
	def appendGame(self,game):
		self.games.append(game)

	def avgScore(self):
		scores = [int(user.score) for user in self.games]
		avg_score = sum(scores) / float(len(scores))
		return avg_score

	def avgTime(self):
		times = [int(user.time) for user in self.games]
		avg_time = sum(times) / float(len(times))
		return avg_time

	def names(self):
		names = [user.user for user in self.games]
		return names

	# Returns a dictionary of tags associated with how many people think it's that tag
	def genreProfile(self):
		tags = [user.tags for user in self.games]
		tags = [item for sublist in tags for item in sublist]
		profile = {}
		for i in tags:
			if i in profile:
				profile[i] += 1
			else:
				profile[i] = 1
		return profile

	# Returns an int representing user and game genre compatibility
	def genreRank(self,user_profile):
		game_profile = self.genreProfile() # amount of people who think it is a certain genre
		rank = 0
		for tag in game_profile:
			if tag in user_profile:
				rank += user_profile[tag] * game_profile[tag]
			else:
				rank += ADVENTURE * game_profile[tag]
		return rank

	# Synthesizes ratings
	def overallRank(self,user_profile):
		genre = self.genreRank(user_profile)
		rating = self.avgScore()
		overall = (genre ** GENRE_FACTOR) * (rating ** RATING_FACTOR)
		return overall

# Represents one user and games associated with him/her
class UserList:
	def __init__(self,name):
		self.name  = name
		self.games = []

	def __repr__(self):
		return repr(self.games)

	def appendGame(self,game):
		self.games.append(game)

	def getTimeData(self):
		time = [(game.time,game.score) for game in self.games]
		avg = sum(i for i,_ in time) / float(len(time))
		timeW = [((t - avg)*(s/float(10))+avg) for (t,s) in time]
		avgC = sum(timeW) / float(len(timeW))
		st = stdev(avgC,timeW)
		return (avgC,st)

	# Return a dictionary of genres the user likes (based on how they rated games of that genre and how many they own)
	def userProfile(self):
		tags = [[(tag,game.score) for tag in game.tags] for game in self.games]
		tags = [item for sublist in tags for item in sublist]
		counts = {}
		for (i,j) in tags:
			if i in counts:
				counts[i] += (j / float(10))
			else:
				counts[i] = (j / float(10))
		return counts


# ************************************************************************
# System functionality
# ************************************************************************


# Calculates standard deviation. Adapted from Python 3's statistics library
def stdev(mean, data):
	s = sum((d-mean)**2 for d in data)
	ss = (s / float(len(data))) ** 0.5
	return ss

# The recommender function! 
def recommend(name):
	user_profile = users[name].userProfile()
	# sort all games (descending) by overall rank given your genre profile
	games_sorted = sorted(games.values(), key=operator.methodcaller('overallRank',user_profile), reverse=True)
	# filter out games you already own
	result = [x for x in games_sorted if name not in x.names()]
	# explain your decision!
	explain(result[0],name,user_profile)

# Explains the decision the recommender made
def explain(game,name,user_profile):
	print "We recommend the game: " + game.name

	# how does it fit with your length profile?
	(time, st) = users[name].getTimeData()
	avgTime = game.avgTime()
	l1 = ""
	l2 = "clocking in at " + str(avgTime) + " hours, we think you'll enjoy it!"
	if (avgTime > time + st):
		l1 = "Despite being longer than most games you've enjoyed, "
	elif (avgTime < time - st):
		l1 = "Despite being shorter than most games you've enjoyed, "
	else:
		l1 = "Since this game seems right up your alley length wise, "
	print l1 + l2

	# What contributed to the recommendation? Let's find out!
	genre = sorted(games.values(), key=operator.methodcaller('genreRank',user_profile), reverse=True)
	genre = [x for x in genre if name not in x.names()]
	for c,x in enumerate(genre):
		if game.name == x.name: # This condition will always be true at some point in list
			genre = c
			break

	score = sorted(games.values(), key=operator.methodcaller('avgScore'), reverse=True)
	score = [x for x in score if name not in x.names()]
	for c,x in enumerate(score):
		if game.name == x.name: # This condition will always be true at some point in list
			score = c
			break
	# score and genre are the ranks (ints) the game selected had by those metrics

	# What was the rating?
	rating_string = ""
	if rating_string == 10:
		rating_string += "perfect "
	rating_string += str(game.avgScore())
	rating_string += "/10" # rating will be either "xx/10" or "perfect 10/10"

	# What are the major genres?
	adventure = True # Set to false if the genres are in my profile
	genre_string = ""
	game_profile = game.genreProfile()
	total = len(game.games)
	game_profile.update({k: (v / float(total)) for k,v in game_profile.items()})
	game_profile = sorted(game_profile.items(), key=operator.itemgetter(1), reverse=True)
	genres_print = []
	for (k,v) in game_profile:
		if v > 0.5:
			genres_print.append(k)
			if k in user_profile:
				adventure = False
	if len(genres_print) == 0:
		genres_print.append(game_profile[0])
		if game_profile[0] in user_profile:
			adventure = False
	for x in genres_print:
		genre_string = genre_string + str(x) + "/"
	genre_string = genre_string[:-1] # genre_string will be slash seperated major genre list

	# Based on which had more impact, let them know why it was selected along with some info
	if adventure:
		print "By our count, you've never played a game of this genre, but the reviews are in, and it's killer! (it's a(n) " + rating_string + ")"
	elif genre > score:
		print "This game really fits your favorite genres (it's a(n) " + genre_string + ") and also comes highly recommended (it's a(n) " + rating_string + ")."
	elif score > genre:
		print "This game has a great overall score (it's a(n) " + rating_string + ") and also matches some of your favorite genres (it's a(n) " + genre_string + ")."
	else:
		print "This game has a great balance of genres for you (it's a(n) " + genre_string + ") and a solid overall score (it's a(n) " + rating_string + ")."

	print "Based on this data, we feel this game would be a good fit for you!"
	print "Be sure to add more games to make your recommendations more accurate and to help other gamers out :)"


# ************************************************************************
# These are methods to maintain the database (a txt file)
# ************************************************************************


def load(filename):
	global users
	global games
	users = {}
	games = {}
	f = open(filename,'r')
	for x in range(int(f.readline().rstrip())):
		name = f.readline().strip()
		users[name] = UserList(name)
		for y in range(int(f.readline().rstrip())):
			title = f.readline().rstrip()
			tags = []
			for z in range(int(f.readline().rstrip())):
				tags.append(f.readline().rstrip())
			score = int(f.readline().rstrip())
			time  = int(f.readline().rstrip())
			users[name].appendGame(Game(name,title,tags,score,time))
			if title not in games:
				games[title] = GameList(title)
			games[title].appendGame(Game(name,title,tags,score,time))
	f.close()

def store(filename):
	f = open(filename,'w')
	f.write(str(len(users)) + '\n')
	for name,games in users.iteritems():
		games = games.games
		f.write(name + '\n')
		f.write(str(len(games)) + '\n')
		for data in games:
			f.write(data.title + '\n')
			f.write(str(len(data.tags)) + '\n')
			for tag in data.tags:
				f.write(tag + '\n')
			f.write(str(data.score) + '\n')
			f.write(str(data.time)  + '\n')
	f.close()

# Allows you to add games to your library
def update(name):
	global users
	global games
	while True:
		game = {}
		user = {}
		title = raw_input("Please enter a game:     ").upper()
		if title in [game.title for game in users[name].games]:
			print("You already input this game!")
			continue
		tags = []
		while True:
			ans = raw_input("Enter a genre tag (or DONE to stop):     ").upper()
			if ans == "DONE":
				break
			tags.append(ans.upper())
		score = int(raw_input("What would you rate this game out of 10?:     "))
		time  = int(raw_input("How long did this take to beat?:     "))
		users[name].appendGame(Game(name,title,tags,score,time))
		if title not in games:
			games[title] = GameList(title)
		games[title].appendGame(Game(name,title,tags,score,time))
		ans = raw_input("Would you like to enter another game?: [y/n]     ")
		if ans == 'n':
			break


# ************************************************************************
# Code to be executed
# ************************************************************************


load('games.txt')

# The application loop
print("Welcome to the Game Recommender by Sam Levatich!")
ans = raw_input("Are you an existing user? [y/n]     ")
if ans == 'y':
	while True:
		ans = raw_input("What is your name?     ").upper()
		if ans in users:
			name = ans
			while True:
				ans = raw_input("What is your quest? [update/recommendation]     ")
				if ans == 'update':
					update(name)
					ans = raw_input("Anything else? [y/n]     ")
					if ans == 'n':
						break
				elif ans == 'recommendation':
					recommend(name)
					ans = raw_input("Anything else? [y/n]     ")
					if ans == 'n':
						break
				else:
					print("Try Again!")
			break
		else:
			ans = raw_input("User not found. Try again? [y/n] ")
			if ans == 'n':
				break
else:
	name = raw_input("Please enter your name:     ").upper()
	users[name] = UserList(name)
	print("Now enter some game data!")
	update(name)
	ans = raw_input("How about a recommendation? [y/n]     ")
	if ans == 'y':
		recommend(name)
		print("Have fun!")
	else:
		print("OK BAI")

store('games.txt')
