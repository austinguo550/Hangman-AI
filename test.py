import preprocess
import os

cwd = os.path.dirname(os.path.realpath(__file__))

def main():
	preprocessor = preprocess.Preprocessor('{}/2-letter-words.json'.format(cwd))	# preprocess is called
	print preprocessor.processedWords

if __name__ == '__main__':
	main()