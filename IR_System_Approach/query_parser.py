from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk
nltk.download('wordnet',quiet=True)
nltk.download('punkt',quiet=True)
nltk.download('averaged_perceptron_tagger',quiet=True)

query= "videos of batting in cricket"

def get_Keywords(text):
	'''
	Description:This function returns an array of keywords.

	input parameter => query sentence
	output => list of keywords

	'''
	tokenized = word_tokenize(text)
	lemmatizer = WordNetLemmatizer()
	tokens = [lemmatizer.lemmatize(token) for token in tokenized] 
	tags = pos_tag(tokenized)
	nouns = [word for word, pos in tags if pos == 'NNP' or pos == 'NN' or pos == 'NNP' or pos == 'NNPS' or pos == 'VBG' or pos == 'VBD' or pos == 'VBP' or pos == 'VBP']
	return nouns

'''
print(get_Keywords(query))
'''