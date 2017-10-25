class Preprocessor:
	processedWords = []

	def __init__(self, wordsFile):
		if '.json' not in wordsFile:
			self.preprocess(wordsFile)
		else:
			self.preprocessJSON(wordsFile)

	def preprocess(self, wordsFile):
		try:
			handle = open(wordsFile)
			self.processedWords = handle.read().lower().split('\n')
			handle.close()
		except:
			print 'Couldnt read file!'

	def preprocessJSON(self, wordsFile):
		try:
			handle = open(wordsFile)
			self.processedWords = handle.read().lower().replace('{\"word\":','').replace('\"','').replace('[','').replace(']','').replace('}','').replace(',','\n').split('\n')
			handle.close()
		except:
			print 'Couldnt read file!'