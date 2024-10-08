import torch.nn as nn
import torch
from config.constants import MODEL_HIDDEN_LAYER_1_UNITS, MODEL_HIDDEN_LAYER_2_UNITS, MODEL_OUTPUT_UNITS

class RegressionModel(nn.Module):
    def __init__(self, input_dim):
        super(RegressionModel, self).__init__()
        self.fc1 = nn.Linear(input_dim, MODEL_HIDDEN_LAYER_1_UNITS)
        self.fc2 = nn.Linear(MODEL_HIDDEN_LAYER_1_UNITS, MODEL_HIDDEN_LAYER_2_UNITS)
        self.fc3 = nn.Linear(MODEL_HIDDEN_LAYER_2_UNITS, MODEL_OUTPUT_UNITS)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x
