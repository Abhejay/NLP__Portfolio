import nltk
import numpy as np
from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()

# Tokenize the sentence
def sentenceTokenize(sentence):
    return nltk.word_tokenize(sentence)

# Get Stem of word
def wordStem(word):
    return stemmer.stem(word.lower())

# Create bag of words
def bagOfWords(tokenizedSentence, allWords):
    tokenizedSentence = [wordStem(word) for word in tokenizedSentence]
    bag = np.zeros(len(allWords), dtype=np.float32)
    for index, w in enumerate(allWords):
        if w in tokenizedSentence:
            bag[index] = 1.0

    return bag
