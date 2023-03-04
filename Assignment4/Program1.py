#Assignment: N Gram Language Model
#Names: Abhejay Murali, Ahmed Iqbal
#Date Due: March 4th, 2023


import nltk
from nltk.util import ngrams
import pickle


#Function with filename as argument
def preprocess(file):

    #Read in text and remove new lines
    contents = open(file, encoding='utf-8').read().replace('\n', '')

    #Tokenize text
    tokens = contents.split()

    #Using NLTK to create bigrams and unigrams list
    bigrams = list(ngrams(tokens, 2))
    unigrams = list(ngrams(tokens, 1))

    #Creating Unigram and Bigram dictionary
    unigram_dict = {t: unigrams.count(t) for t in set(unigrams)}
    bigram_dict = {b: bigrams.count(b) for b in set(bigrams)}

    #Returning dictionaries
    return unigram_dict, bigram_dict



if __name__ == '__main__':

    #Call the functions for each training file in 3 different languages
    englishUnigram, englishBigram = preprocess('data/LangId.train.English')
    frenchUnigram, frenchBigram = preprocess('data/LangId.train.French')
    italianUnigram, italianBigram = preprocess('data/LangId.train.Italian')

    #Pickling the 6 dictionaries

    with open('englishUnigram.pickle', 'wb') as handle:
        pickle.dump(englishUnigram, handle)

    with open('englishBigram.pickle', 'wb') as handle:
        pickle.dump(englishBigram, handle)

    with open('frenchUnigram.pickle', 'wb') as handle:
        pickle.dump(frenchUnigram, handle)

    with open('frenchBigram.pickle', 'wb') as handle:
        pickle.dump(frenchBigram, handle)

    with open('italianUnigram.pickle', 'wb') as handle:
        pickle.dump(italianUnigram, handle)

    with open('italianBigram.pickle', 'wb') as handle:
        pickle.dump(italianBigram, handle)
