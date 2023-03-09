#Assignment: Web Crawler
#Name: Abhejay Murali
#Date Due: March 11th, 2023

"""

When running the program, just quick information on how to run.
-----------------------------------------------------------------------------------------------------------------
- Run each function separately as the program tends to take a long time to run all functions.
- The program will run most of the time if you run all functions, but sometimes the http request might time out.
    you can re-run or run each method separately to make sure it works.

"""


import urllib.request
from os import listdir
from os.path import isfile, join
import requests
from bs4 import BeautifulSoup
import nltk
import re
import pickle
from nltk.corpus import stopwords

#Function that outputs list of relevant URLs by crawling through website
def webCrawler(url):

    #Make request to url and store text
    webText = requests.get(url).text
    soup = BeautifulSoup(webText, 'html.parser')

    #List of unnecessary and relevant words used to classify links
    unnecessary_words = ['cite', 'nytimes', 'archive', 'telegraph', 'tvnz', 'hoopedia', 'books', 'jpg']
    relevant_words = ['court', 'shot', 'dunk', 'layup', 'nba', 'dribbling', 'shooting', 'rebound']

    #URLs that are gathered based on requirements
    URLS = []

    #Loop and look for links with 'a' and 'href' html tags
    for link in soup.find_all('a'):
        strLink = str(link.get('href'))

        #If word is unnecessary skip
        if any(unnecessary in strLink for unnecessary in unnecessary_words):
            continue

        #If word is relevant in link
        if any(relevant in strLink for relevant in relevant_words):
            if strLink.startswith('#'):
                URLS.append(url + strLink)
            if strLink.startswith('/'):
                URLS.append(url[:24] + strLink)
            if strLink.startswith('http'):
                if strLink not in URLS:
                    try:
                        urllib.request.urlopen(strLink) # Check if link works
                    except urllib.error.URLError:
                        continue
                    URLS.append(strLink)

        #Add 25 URLs
        if len(URLS) == 25:
            break


    #Create a set of the URLs to make sure they are unique
    uniqueURLS = set(URLS)
    relevantURLS = list(uniqueURLS)

    #Return the unique URLs
    return relevantURLS


#Scrape all the text off of the webpages and store each file inside folder webpages/
def urlScrape(urls):
    #Loop through every link in the URLs
    for i, link in enumerate(urls):
        #Send request for link and store text
        webText = requests.get(link).text
        sp = BeautifulSoup(webText, 'html.parser')

        #Check style tags in html and remove
        for tag in sp():
            for attribute in ['style']:
                del tag[attribute]

        #Get the raw text from webpage
        txt = sp.get_text()

        #Write into a file with encoding utf-8
        f = open('webpages/' + str(i+1) + 'website.txt', 'w', encoding='utf-8')
        f.write(txt)

#Gather the sentences from the raw text files
def cleanText():

    #List of files in the folder webpages
    files = [f for f in listdir('webpages') if isfile(join('webpages', f))]
    count = 1

    #Loop through the files
    for file in files:

        #Look through the content and remove new lines and tabs
        contents = open('webpages/' + file, encoding='utf-8').read().replace('\n', '').replace('\t', '')

        #Tokenize the sentences using NLTK
        sent = nltk.sent_tokenize(contents)

        #Output the sentences into separate files for each webpage and store in the directory sentences/
        with open('sentences/' + str(count) + 'sentences.txt', 'w', encoding='utf-8') as f:
            for sentence in sent:
                f.write(sentence)
                f.write('\n')

        count += 1

#Extract the important terms from each page
def importantTerms():
    #NLTK stopwords
    sw = set(stopwords.words('english'))

    #List of files in the folder sentences
    files = [f for f in listdir('sentences') if isfile(join('sentences', f))]
    count = 1

    #List for output of frequent words
    frequentOutput = []

    #Loop through the files
    for file in files:

        #Tokens of values that are the most frequent
        tokens = []

        #Read lines in the sentences files
        sentences = open('sentences/' + file, encoding='utf-8').readlines()
        for sentence in sentences:   # For every sentence in the file
            sen = re.sub(r'[^\w\s]', '', sentence)   # Remove punctuation using regular expressions
            tokens += nltk.word_tokenize(sen)  # Tokenize the words in the sentence

        #remove stop words and lower case
        stops = [w for w in tokens if not w.lower() in sw]
        frequency = nltk.FreqDist(stops)

        #Extract 25 most common words
        frequent = frequency.most_common(25)

        #Output 2 most common words
        frequentOutput.append(frequency.most_common(3))

        #Pickle the list of frequent words for each page and store the files in the directory words/
        with open('words/' + str(count) + '-important-words.pickle', 'wb') as handle:
            pickle.dump(frequent, handle)

        count += 1

    #Pickle most frequent words across all pages
    with open('words/all-important-words.pickle', 'wb') as handle:
        pickle.dump(frequentOutput, handle)

    #Output the terms
    print('25-40 IMPORTANT TERMS')
    print('------------------------')
    uniqueWords = []
    for list in frequentOutput:
        for word in list:
            if word[0] not in uniqueWords:
                uniqueWords.append(word[0])
                print(word[0].lower())

    print('TOTAL WORDS:', len(uniqueWords))


#The knowledge base for chatbot
def knowledgeBase():

    #Top 10 terms
    terms = ['basketball', 'nba', 'wnba', 'threepoint', 'court', 'baseline', 'player', 'defender', 'dunk', 'ball']

    #Ten terms from basketball based on my domain knowledge
    knowledge = {
        'basketball': 'a game played between two teams of five players in which goals are scored by throwing a ball through a netted hoop fixed above each end of the court.',
        'nba': 'The National Basketball Association is the major professional basketball league in the United States.',
        'wnba': 'The Women National Basketball Association is a professional basketball league comprised of 12 teams featuring the best women basketball players in the world.',
        'threepoint': 'A field goal in a basketball game made from beyond the three-point line, a designated arc surrounding the basket.',
        'court': 'The playing surface , consisting of a rectangular floor, with baskets at each end.',
        'baseline': 'The baseline runs from sideline to sideline behind the backboard at the ends of the court.',
        'player': 'An athlete who plays basketball',
        'defender': 'Defender is the player who guards his basket from the opposite team.',
        'dunk': 'A scoring shot in which a player jumps up and forces the ball down through the basket.',
        'ball': 'The NBA game ball is made of a leather that comes exclusively from the Horween Leather Company in Chicago.'
    }

    #Pickle the knowledge base and store in directory knowledge/
    with open('knowledge/knowledge-base.pickle', 'wb') as handle:
        pickle.dump(knowledge, handle)


if __name__ == '__main__':

    #Website to initiate the web crawler
    initialLink = 'https://en.wikipedia.org/wiki/Basketball'

    #Web Crawler Function
    relevant_links = webCrawler(initialLink)
    print(relevant_links)
    print('NUMBER OF LINKS:', len(relevant_links))

    #Rest of functions
    urlScrape(relevant_links)
    cleanText()
    importantTerms()
    knowledgeBase()
