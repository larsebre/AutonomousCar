from tkinter import *
import numpy as np
import Car as c
import Map as m
import Perceptron as p
import random
import time
import sys
import copy

sys.setswitchinterval(100)

window = Tk()
canvas_width = 2000
canvas_height = 1000

cvs = Canvas(window, height=canvas_height, width=canvas_width, bg = 'light grey')
cvs.pack()


#########
frequency = 60.0 # Hz
period = 1.0/frequency

counter = 0

map = m.Map(cvs=cvs)
map.print_map()
cars = []

#Generate neural network

input_layer = (1 - (np.random.rand(3,5) * 2))
hidden_layer = (1 - (np.random.rand(4,3) * 2))
output_layer = (1 - (np.random.rand(2,4) * 2))

print(input_layer)

brain = p.NeuralNetwork(input_layer, hidden_layer, output_layer)
new_brain = copy.copy(brain)
best_distance = 0

def max(a,b):
    if (a>b):
        return a
    return b


while True:

    new_generation = False

    brain = new_brain

    for i in range(10):
        cars.append(c.Car(140, 700, cvs))

    for i in range(len(cars)):
        cars[i].brain = copy.copy(brain)

    # Add one random car each generation, with no enharitage from the others

    car1 = c.Car(140, 700, cvs)
    car1.brain = p.NeuralNetwork((1 - (np.random.rand(3,5) * 2)), (1 - (np.random.rand(4,3) * 2)), (1 - (np.random.rand(2,4) * 2)))
    cars.append(car1)
    car2 = c.Car(140, 700, cvs)
    car2.brain = p.NeuralNetwork((1 - (np.random.rand(3, 5) * 2)), (1 - (np.random.rand(4, 3) * 2)),
                                 (1 - (np.random.rand(2, 4) * 2)))
    cars.append(car2)


    for i in range(len(cars)):
        cars[i].brain.randomize_weights()

    outputs = [[[0], [0]]] * len(cars)

    start_over = False

    while (new_generation == False):
        time_before = time.time()
        counter = counter + 1

        for i in range(len(cars)):

            if (cars[i].crash == False):
                omega = 50 * np.tanh(outputs[i][1][0])
                thrust = 10000 + cars[0].u_max / (1 + np.exp(-outputs[i][0][0]))
                cars[i].calc_dynamics(thrust, omega)
                cars[i].calc_transelation(omega)
                cars[i].update_sensor_values(map.map_lines)
                cars[i].check_crash()
                outputs[i] = cars[i].brain.calculate_outputs(np.array([[cars[i].sensor_left_data[2]], [cars[i].sensor_left_up_data[2]], [cars[i].sensor_right_data[2]],[cars[i].sensor_right_up_data[2]], [cars[i].sensor_up_data[2]]]))
        

        if (counter == 2):
            # Manage 50Hz screen update, 50FPS
            for i in range(len(cars)):
                cars[i].rotate_car()
                cars[i].update_car()

            window.update()
            counter = 0


        check = 0
        for i in range(len(cars)):
            if (cars[i].crash == True):
                check = check + 1

        if (check == len(cars)):
            for i in range(len(cars)):
                if (cars[i].distance > best_distance):
                    best_distance = cars[i].distance
                    new_brain = cars[i].brain
                cars[i].delete_car()

            cars.clear()
            new_generation = True


        while (time.time() - time_before) < period:
            time.sleep(0.00001)  # precision here


