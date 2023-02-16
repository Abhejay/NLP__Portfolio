# Assignment: Homework 2
# Name: Abhejay Murali (AXM180115)
# Date Due: 2-18-2023


import random
import sys
import pathlib
import re
import pickle
import nltk
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords


# Function to preprocess the raw text
def preprocess(tokens):
    # Tokenize to lower case, reduce tokens to only those that are alpha, not in stopwords list, and length > 5
    processedTokens = [t.lower() for t in tokens]
    processedTokens = [t for t in processedTokens if t.isalpha() and t not in stopwords.words('english') and len(t) > 5]

    # Lemmatize the tokens and make list of unique lemmas
    wnl = WordNetLemmatizer()
    lemmas = [wnl.lemmatize(t) for t in processedTokens]
    lemmas_unique = list(set(lemmas))

    # Part of speech tagging and printing first 20 tagged
    lemmas_unique = nltk.pos_tag(lemmas_unique)
    print('First 20 tagged words: ', lemmas_unique[:20])

    # List of lemmas that are nouns
    lemmas = nltk.pos_tag(lemmas)
    uniqueNounLemmas = []
    nounLemmas = []
    for noun in lemmas:
        if noun[1] == 'NN':
            nounLemmas.append(noun)

    for noun in lemmas_unique:
        if noun[1] == 'NN':
            uniqueNounLemmas.append(noun)

    # Print # of tokens and nouns
    print('len of tokens after preprocessing', len(processedTokens))
    print('len of nouns after preprocessing', len(uniqueNounLemmas))

    # Return tokens, nouns
    return processedTokens, nounLemmas


#Output the list for guessing game
def listOutput(word):
    for i in word:
        print(i, end = ' ')


#Check if the user's guessed word matches the unknown word
def wordMatch(word, unknownWord):
    for i in range(len(word)):
        if word[i] != unknownWord[i]:
            return False

    return True


#Run the guessing game by taking in a list of words
def guessGame(words):
    score = 5
    userGuess = ''

    # Randomly choose one of the top 50 words
    res = random.choice(words)

    # Create unknown word fill-in-blank list and output to console
    unknownWord = []
    for i in range(len(res)):
        unknownWord.append('_')

    listOutput(unknownWord)

    while True:
        correctGuess = False

        # User guesses a letter and exit game if user enter '!'
        userGuess = input('\nGuess a letter: ').lower()
        if userGuess == '!':
            return

        # Check if the user guessed correctly
        for i in range(len(res)):
            if userGuess == res[i]:
                unknownWord[i] = userGuess
                correctGuess = True

        # Increase or decrease score depending on the input
        if correctGuess == True:
            score += 1
            print('Right! Score is', score)
        if correctGuess == False:
            score -= 1
            if score < 0:
                return
            print('Sorry, guess again. Score is', score)

        # Output list
        listOutput(unknownWord)

        # If the user guesses the word correctly, create another random word and restart the game
        if wordMatch(res, unknownWord):
            print('\nYou solved it!')
            print('\nCurrent score:', score)
            print('\nGuess another word')
            res = random.choice(words)
            unknownWord = []
            for i in range(len(res)):
                unknownWord.append('_')
            listOutput(unknownWord)


#Main Function
if __name__ == '__main__':

    # Read File
    if len(sys.argv) > 1:
        arg_input = sys.argv[1]
        print('Input file: ', arg_input)
    else:
        print('File name missing')

    # Read raw text from file
    with open(arg_input) as f:
        contents = f.read()

    # Tokenize Text
    tokens = nltk.word_tokenize(contents)

    # Calculate Lexical Diversity
    print("Lexical diversity: %.2f" % (len(set(tokens)) / len(tokens)))
    print()

    # Get return values from text preprocessing
    processedTokens, nouns = preprocess(tokens)

    print('\n50 most common words:')

    # Dictionary of noun keys with value attribute of count
    # Sort the dictionary
    countNouns = {t[0]: nouns.count(t) for t in nouns}
    sortedCountNounsList = sorted(countNouns.items(), key=lambda x: x[1])
    sortedCountNouns = dict(sortedCountNounsList)

    # Output the first 50 most common words and their count
    counter = 0
    frequentNouns = []
    for val in reversed(sortedCountNouns.items()):
        if counter == 50:
            break

        print(val)
        frequentNouns.append(val[0])
        counter += 1

    # Call the guessing game function to play
    print('\nLet play a word guessing game!')
    guessGame(frequentNouns)
