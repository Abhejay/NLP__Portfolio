import random
import json
import torch
import spacy

spacy.cli.download("en_core_web_sm")
spacy.cli.link("en_core_web_sm", "en", force=True)

from UserModel import UserModel
from model import NeuralNet
from preprocess import bagOfWords, sentenceTokenize

# Where to run
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Open the intents file and load the data
with open('intents/intents.json', 'r') as json_data:
    intents = json.load(json_data)

# Load trained model into pytorch
FILE = 'Trained_Data/data.pth'
data = torch.load(FILE)

# Get content from trained model output
inputSize = data['input_size']
hiddenSize = data['hidden_size']
outputSize = data['output_size']
allWords = data['all_words']
tags = data['tags']
modelState = data['model_state']

# Load model state and evaluate
model = NeuralNet(inputSize, hiddenSize, outputSize).to(device)
model.load_state_dict(modelState)
model.eval()

botName = 'Java'

# Load spacy library and terms for getting likes and dislikes
nlp = spacy.load('en_core_web_sm')
coffee_terms = ['americano', 'espresso', 'latte', 'cappuccino', 'mocha']
likes_terms = ['enjoy', 'like', 'love', 'want']
dislike_terms = ['dislike', 'hate', 'despise', 'reject', 'do not like']

# Conversations with the user
conversationalQuestions = [
    'Quick question, is there a specific coffee you LIKE in my knowledge base?',
    'Quick question, is there a specific coffee you do NOT LIKE in my knowledge base?'
]

# Likes and dislikes of the user
userLikes = []
userDislikes = []

# Check if the user has ever used the bot before
userExists = input('Do you have an account (Y/N): ')
if userExists == 'Y':
    username = input('Username: ')
    age = input('Age: ')
    user = UserModel(username, age)
else:
    username = input('Enter a username: ')
    age = input('Enter an age: ')
    user = UserModel(username, age)

# Initial instructions
print('Java The Coffee Bot')
print('I am an expert in the Latte, Cappuccino, Espresso, Americano, and Mocha')
print('You can ask me the WHAT, ORIGIN, VARIATIONS, RECIPES, MILK, and CALORIES')
print('-------------------------------------------------------------------------------------------------------')

# If user already has account, retrieve their previous remarks
userPastLikes, userPastDislikes = user.getPersonalizedRemark()

if userExists == 'Y':
    print(f'Welcome Back {username}! I remember from our previous conversations what you liked: ')
    for like in userPastLikes:
        print('-> ', like)
    print('Let us chat! (Type QUIT or BYE to leave)')
elif userExists == 'N':
    print(f'Welcome {username}! Go ahead I am listening!')
    print('Let us chat! (Type QUIT or BYE leave)')


count = 0

# Interacting with the chatbot
while True:
    sentence = input(f"{username}: ")
    if sentence == "quit" or sentence == 'QUIT' or sentence == 'BYE' or sentence == 'bye':
        print('BYE!')
        break

    for dislike in userPastDislikes:
        if dislike in sentence:
            print(f'{botName}: I remember you told me you do not like this!')

    doc = nlp(sentence)

    questionAnswered = False
    for token in doc:
        if (token.text.lower() in coffee_terms) and (token.head.text.lower() in likes_terms):
            print(f'{botName}: Hey that is good information! I will make sure to remember :)')
            userLikes.append(token)
            questionAnswered = True
        elif (token.text.lower() in coffee_terms) and (token.head.text.lower() in dislike_terms):
            print(f'{botName}: I will make sure to remember your taste.')
            userDislikes.append(token)
            questionAnswered = True

    if questionAnswered:
        continue

    sentence = sentenceTokenize(sentence)
    X = bagOfWords(sentence, allWords)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                print(f"{botName}: {random.choice(intent['responses'])}")
                count += 1

                if count % 3 == 0:
                    random_index = random.randint(0, len(conversationalQuestions) - 1)
                    randomQuestion = conversationalQuestions[random_index]
                    print(f'{botName}: ', randomQuestion)
    else:
        print(f"{botName}: I do not understand... Can you re-phrase please :(")


# Adding the likes into the new account or update the previous account of the user based on interaction
likes_serializable = [token.text for token in userLikes]
dislikes_serializable = [token.text for token in userDislikes]

user.updateLikes(likes_serializable)
user.addDislikes(dislikes_serializable)

if userExists == 'Y':
    user.updateCredential()
else:
    user.createCredentials()


