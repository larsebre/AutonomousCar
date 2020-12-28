import numpy as np
import random


class NeuralNetwork:

    def __init__(self, input_layer, hidden_layer, output_layer, gain):

        self.gain = gain

        self.input_layer = input_layer * self.gain * 1.0
        self.hidden_layer = hidden_layer * self.gain * 12
        self.output_layer = output_layer * self.gain * 0.5


    def calculate_outputs(self, inputs):
        output = np.matmul(self.input_layer, inputs)
        output = np.matmul(self.hidden_layer, output)
        output = np.matmul(self.output_layer, output)

        return output

    def randomify_weights(self):
        self.input_layer = self.input_layer + (1 - (np.random.rand(3, 5) * 2)) * self.gain * 0.1 * 3
        self.hidden_layer = self.hidden_layer + (1 - (np.random.rand(4, 3) * 2)) * self.gain * 1.2 * 3
        self.output_layer = self.output_layer + (1 - (np.random.rand(2, 4) * 2)) * self.gain * 0.1 * 3


