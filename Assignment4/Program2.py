#Assignment: N Gram Language Model
#Names: Abhejay Murali, Ahmed Iqbal
#Date Due: March 4th, 2023


import pickle
import nltk
from nltk.util import ngrams

#Calculate the probability
def compute_prob(text, unigram_dict, bigram_dict, V):

    #Get the unigrams and bigrams in the line of the test data
    unigrams_test = nltk.word_tokenize(text)
    bigrams_test = list(ngrams(unigrams_test, 2))

    #Calculate the probability using laplace smoothing
    p_laplace = 1
    for bigram in bigrams_test:
        n = bigram_dict[bigram] if bigram in bigram_dict else 0
        d = unigram_dict[bigram[0]] if bigram[0] in unigram_dict else 0
        p_laplace = p_laplace * ((n + 1) / (d + V))

    #Return the probability
    return p_laplace



if __name__ == '__main__':

    #Reading in the pickled dictionaries

    with open('englishUnigram.pickle', 'rb') as handle:
        englishUnigram = pickle.load(handle)

    with open('englishBigram.pickle', 'rb') as handle:
        englishBigram = pickle.load(handle)

    with open('frenchUnigram.pickle', 'rb') as handle:
        frenchUnigram = pickle.load(handle)

    with open('frenchBigram.pickle', 'rb') as handle:
        frenchBigram = pickle.load(handle)

    with open('italianUnigram.pickle', 'rb') as handle:
        italianUnigram = pickle.load(handle)

    with open('italianBigram.pickle', 'rb') as handle:
        italianBigram = pickle.load(handle)


    #Read test file and create list of lines
    testFileLines = open('data/LangId.test', 'r')
    testLines = testFileLines.readlines()
    testFileLines.close()

    #Create output file
    outputFile = open('data/output.txt', 'w')

    #Total unigram size for each language
    v_english = len(englishUnigram)
    v_french = len(frenchUnigram)
    v_italian = len(italianUnigram)

    #Use enumerate function to get line numbers
    for line_num, line in enumerate(testLines):

        #Calculate probabilities for each language passing in the parameters
        prob_eng = compute_prob(line, englishUnigram, englishBigram, v_english)
        prob_fre = compute_prob(line, frenchUnigram, frenchBigram, v_french)
        prob_ita = compute_prob(line, italianUnigram, italianBigram, v_italian)

        #Write the language with the highest probability to the output file
        if max(prob_eng, prob_fre, prob_ita) == prob_eng:
            outputFile.write(str(line_num + 1) + ' English\n')
        elif max(prob_eng, prob_fre, prob_ita) == prob_fre:
            outputFile.write(str(line_num + 1) + ' French\n')
        elif max(prob_eng, prob_fre, prob_ita) == prob_ita:
            outputFile.write(str(line_num + 1) + ' Italian\n')

    outputFile.close()

    #Read in the correct and system classification into lists
    correctClassification = open('data/LangId.sol', 'r')
    systemClassification = open('data/output.txt', 'r')
    correctClassification_lines = correctClassification.readlines()
    systemClassification_lines = systemClassification.readlines()

    #Track the correct and incorrect line while also holding the total number of classifications
    correct = 0
    incorrect = []
    total = len(correctClassification_lines)

    #Iterate through the lines to see the number of lines that match between correct and system classification
    for line_num, line in enumerate(correctClassification_lines):
        if line == systemClassification_lines[line_num]:
            correct += 1
        else:
            incorrect.append(line_num)

    #Output accuracy and the incorrect lines
    accuracy = 100 * ((total - len(incorrect)) / total)
    print('Accuracy: %.5f' % accuracy + '%')
    print('Incorrect line numbers:', incorrect)