import json
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

from preprocess import sentenceTokenize, wordStem, bagOfWords
from model import NeuralNet

# Open intents JSON for data
with open('intents/intents.json', 'r') as f:
    intents = json.load(f)

# Variables to hold the words, tags, and xy pair from the JSON file
allWords = []
tags = []
xy = []

# Check every sentence in intents JSON
for intent in intents['intents']:
    tag = intent['tag']
    tags.append(tag)
    for inputs in intent['input']:
        w = sentenceTokenize(inputs)
        allWords.extend(w)
        xy.append((w, tag))

# Ignore these punctuation markers and only hold unique values of words and tags
ignoreWords = ['?', '!', '.', ',']
allWords = [wordStem(word) for word in allWords if word not in ignoreWords]
allWords = sorted(set(allWords))
tags = sorted(set(tags))

# Create training data
X_train = []
y_train = []

# Get the bag of words for each sentence
for (inputSentence, tag) in xy:
    bag = bagOfWords(inputSentence, allWords)
    X_train.append(bag)

    label = tags.index(tag)
    y_train.append(label)

X_train = np.array(X_train)
y_train = np.array(y_train)



class ChatData(Dataset):
    def __init__(self):
        self.n_samples = len(X_train)
        self.x_data = X_train
        self.y_data = y_train

    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    def __len__(self):
        return self.n_samples


# Hyperparameters for training
batchSize = 8
hiddenSize = 8
outputSize = len(tags)
inputSize = len(X_train[0])
learningRate = 0.001
epochs = 1000

dataset = ChatData()
trainLoader = DataLoader(dataset=dataset, batch_size=batchSize, shuffle=True, num_workers=0)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = NeuralNet(inputSize, hiddenSize, outputSize).to(device)

# Loss and optimization
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learningRate)

# Training the model for 1000 epochs
for epoch in range(epochs):
    for (words, labels) in trainLoader:
        words = words.to(device)
        labels = labels.to(device)

        outputs = model(words)
        loss = criterion(outputs, labels.long())

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    if (epoch+1) % 100 == 0:
        print(f'epoch {epoch+1}/{epochs}, loss={loss.item():.4f}')

print(f'final loss, loss={loss.item():.4f}')

# Store the data in data.pth file
data ={
    'model_state': model.state_dict(),
    'input_size': inputSize,
    'output_size': outputSize,
    'hidden_size': hiddenSize,
    'all_words': allWords,
    'tags': tags
}

FILE = 'Trained_Data/data.pth'
torch.save(data, FILE)

print(f'training complete. File saved to {FILE}')

