import numpy as np
import random

def constraint(array, val):

    for i in range(len(array)):
        for j in range(len(array[i])):

            if (array[i][j] > val):
                array[i][j] = val
            if (array[i][j] < -val):
                array[i][j] = -val

class NeuralNetwork:

    def __init__(self, input_layer, hidden_layer, output_layer):

        self.input_layer = input_layer
        self.hidden_layer = hidden_layer
        self.output_layer = output_layer


    def calculate_outputs(self, inputs):
        output = np.matmul(self.input_layer, inputs)
        output = np.matmul(self.hidden_layer, output)
        output = [[0.7 * np.tanh(output[0][0])], [0.7 * np.tanh(output[1][0])], [0.7 * np.tanh(output[2][0])], [0.7 * np.tanh(output[3][0])]]
        #output = [[1/(1 + np.exp(-output[0][0]))], [1/(1 + np.exp(-output[1][0]))], [1/(1 + np.exp(-output[2][0]))], [1/(1 + np.exp(-output[3][0]))]]
        output = np.matmul(self.output_layer, output)

        return output

    def randomize_weights(self):

        self.input_layer = self.input_layer + (1 - (np.random.rand(3, 5) * 2)) * 0.2
        self.hidden_layer = self.hidden_layer + (1 - (np.random.rand(4, 3) * 2)) * 0.2
        self.output_layer = self.output_layer + (1 - (np.random.rand(2, 4) * 2)) * 0.2

        constraint(self.input_layer, 1.0)
        constraint(self.hidden_layer, 1.0)
        constraint(self.output_layer, 1.0)


