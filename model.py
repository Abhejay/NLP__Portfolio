import torch.nn as nn

# Neural Net model for training
class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(NeuralNet, self).__init__()
        self.layerOne = nn.Linear(input_size, hidden_size)
        self.layerTwo = nn.Linear(hidden_size, hidden_size)
        self.layerThree = nn.Linear(hidden_size, num_classes)
        self.relu = nn.ReLU()

    def forward(self, x):
        out = self.layerOne(x)
        out = self.relu(out)
        out = self.layerTwo(out)
        out = self.relu(out)
        out = self.layerThree(out)

        return out