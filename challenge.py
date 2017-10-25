import json, requests, preprocess
import collections, random, operator
import os

# first GET request at http://gallows.hulu.com/play?code=austinguo550@ucla.edu
# second-last GET request at http://gallows.hulu.com/play?code=austinguo550@ucla.edu&token=TOKEN&guess=GUESS

wordDict = []
cwd = os.path.dirname(os.path.realpath(__file__))
VOWELS = ['a', 'e', 'i', 'o', 'u']

class Game:

	''' json object contains '''
	TOKEN = ''	# ID for specific instance of the game (pass on all follow up calls)
	STATUS = ''	# ALIVE, DEAD, FREE
	STATE = ''	# shows phrase need to guess, letters guessed show up
	REMAINING_GUESSES = ''	# how many guesses I have left
	gamesWon = 0
	gamesPlayed = 0
	# guessHist = set()
	unguessed = set()
	bestGuesses = []

	def __init__(self):
		self.startGame()

	def startGame(self):
		self.gamesPlayed = self.gamesPlayed + 1
		# self.guessHist = set()
		self.resetUnguessed()
		response0 = requests.get('http://gallows.hulu.com/play?code=austinguo550@ucla.edu').json()
		self.TOKEN = response0['token']
		self.STATUS = response0['status']
		self.STATE = response0['state']
		self.REMAINING_GUESSES = response0['remaining_guesses']
		# AI work
		self.setBestGuesses()
		# Feedback
		print 'Win rate={}'.format(self.winRate())
		print 'GAME STARTED: Token={}, Status={}, State={}, Remaining guesses={}'.format(self.TOKEN, self.STATUS, self.STATE, self.REMAINING_GUESSES)

	def guess(self, GUESS):
		response = requests.post('http://gallows.hulu.com/play?code=austinguo550@ucla.edu&token={}&guess={}'.format(self.TOKEN, GUESS)).json()
		self.TOKEN = response['token']
		self.STATUS = response['status']
		self.STATE = response['state']
		self.REMAINING_GUESSES = response['remaining_guesses']
		# add to guess history, remove from unguessed
		# self.guessHist.add(GUESS)
		self.unguessed.discard(GUESS)
		# feedback
		print 'Token={}, Status={}, State={}, Remaining guesses={}'.format(self.TOKEN, self.STATUS, self.STATE, self.REMAINING_GUESSES)
		# if this was last guess, restart
		if self.STATUS == 'DEAD':	#  lost
			self.startGame()
		elif self.STATUS == 'FREE':	#  won
			gamesWon = gamesWon + 1
			self.startGame()

	def winRate(self):
		if not self.gamesPlayed:
			return 0
		return self.gamesWon / self.gamesPlayed

	# def getGuesses(self):
	# 	return self.guessHist

	def getState(self):
		return self.STATE

	def resetUnguessed(self):
		self.unguessed = set(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v','w', 'x', 'y', 'z'])

	def setBestGuesses(self):	# most probable letter frequencies based on length of word
		# print 'WORD DICT={}'.format(wordDict)
		anonWords = self.STATE.split()
		anonWordsLen = set()
		for word in anonWords:
			anonWordsLen.add(len(word))
		charFrequencies = collections.defaultdict(int)
		vowels = collections.defaultdict(list)
		for word in wordDict:
			if len(word) in anonWordsLen:
				for ch in word:
					if not ch.isalpha():
						continue
					if ch in VOWELS and ch not in vowels:
						vowels[ch].append(1)	# least freq to most freq, will be reversed after
						continue
					if ch in charFrequencies.keys():
						charFrequencies[ch] = charFrequencies[ch] + 1
					else:
						charFrequencies[ch] = 1
		for vowel in vowels.keys():
			vowels[vowel] = len(vowels[vowel])
		vowels = collections.deque(dict(sorted(vowels.items(), key=operator.itemgetter(1), reverse=True)).keys())
		tempDeque = collections.deque(dict(sorted(charFrequencies.items(), key=operator.itemgetter(1))).keys())
		print vowels
		for vowel in vowels:
			tempDeque.appendleft(vowel)
		self.bestGuesses = list(tempDeque)
		print 'BEST GUESSES={}'.format(self.bestGuesses)
		
	def getNextBestGuess(self):
		for guess in self.bestGuesses:
			if guess in self.unguessed:
				return guess
		return random.sample(self.unguessed, 1)[0]	# grab random character, impossible for all characters to be guessed w/o answer so never throws error



def main():
	# preprocessor = preprocess.Preprocessor('{}/words.txt'.format(cwd))	# preprocess is called
	preprocessor2 = preprocess.Preprocessor('{}/2-letter-words.json'.format(cwd))
	preprocessor3 = preprocess.Preprocessor('{}/3-letter-words.json'.format(cwd))
	preprocessor4 = preprocess.Preprocessor('{}/4-letter-words.json'.format(cwd))
	preprocessor5 = preprocess.Preprocessor('{}/5-letter-words.json'.format(cwd))
	preprocessor6 = preprocess.Preprocessor('{}/6-letter-words.json'.format(cwd))
	preprocessor7 = preprocess.Preprocessor('{}/7-letter-words.json'.format(cwd))
	preprocessor8 = preprocess.Preprocessor('{}/8-letter-words.json'.format(cwd))
	preprocessor9 = preprocess.Preprocessor('{}/9-letter-words.json'.format(cwd))
	preprocessor10 = preprocess.Preprocessor('{}/10-letter-words.json'.format(cwd))
	preprocessor11 = preprocess.Preprocessor('{}/11-letter-words.json'.format(cwd))
	preprocessor12 = preprocess.Preprocessor('{}/12-letter-words.json'.format(cwd))
	vocabpreprocessor = preprocess.Preprocessor('{}/vocab.txt'.format(cwd))
	global wordDict
	'''preprocessor.processedWords +'''
	wordDict = preprocessor2.processedWords + preprocessor3.processedWords + preprocessor4.processedWords + preprocessor5.processedWords + preprocessor6.processedWords + preprocessor7.processedWords + preprocessor8.processedWords + preprocessor9.processedWords + preprocessor10.processedWords + preprocessor11.processedWords + preprocessor12.processedWords + vocabpreprocessor.processedWords
	# set the word dict so the game can find the best guesses
	# print 'PROCESSED WORDS={}'.format(preprocessor.processedWords)
	game = Game()	# starts the game

	while 1:
			GUESS = game.getNextBestGuess()
			game.guess(GUESS)
	# try:
	# 	while 1:
	# 		GUESS = game.getNextBestGuess()
	# 		game.guess(GUESS)
	# except:
	# 	print '\nGAME ENDED'
	return 0

if __name__ == '__main__':
	main()