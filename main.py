from tkinter import *
import numpy as np
import Car as c
import Map as m
import NeuralNetwork as p
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
map.load_maps('.../CarTracks.txt')
cars = []

#Generate neural network
input_layer = (1 - (np.random.rand(3,5) * 2))
hidden_layer = (1 - (np.random.rand(4,3) * 2))
output_layer = (1 - (np.random.rand(2,4) * 2))

brain = p.NeuralNetwork(input_layer, hidden_layer, output_layer)
new_brain = copy.copy(brain)
new_brain1 = copy.copy(brain)
best_distance = 0
generation = 1

def max(a,b):
    if (a>b):
        return a
    return b

variance_in_cars_brain = 0.3

while True:

    #Change maps
    map.erase_map()
    map_index = random.randint(0, len(map.map_lines) - 1)
    current_map = map.map_lines[map_index]
    map.print_map(map_index)
    start_koord = map.starts[map_index]
    goal_koord = map.goals[map_index]

    new_generation = False

    brain = copy.copy(new_brain)
    brain1 = copy.copy(new_brain1)

    number_of_cars = 28

    for i in range(number_of_cars):
        cars.append(c.Car(start_koord[0], start_koord[1], cvs))

    for i in range(len(cars)):
        if (i < 21):
            cars[i].brain = copy.copy(brain)
        else:
            cars[i].brain = copy.copy(brain1)

    #Adding variance to the inherited "brain"
    for i in range(len(cars)):
        if (i < 11):
            cars[i].brain.randomize_weights(variance_in_cars_brain)
        elif ((i >= 11) and (i < 20)):
            cars[i].brain.randomize_weights(variance_in_cars_brain / 5.0)
        else:
            cars[i].brain.randomize_weights(variance_in_cars_brain / 2.0)

    outputs = [[[0], [0]]] * len(cars)

    start_over = False

    while (new_generation == False):
        time_before = time.time()

        for i in range(len(cars)):

            if (cars[i].crash == False):
                omega = 50 * np.tanh(outputs[i][1][0])
                thrust = 6000 + cars[i].u_max * np.tanh(outputs[i][0][0])
                cars[i].calc_dynamics(thrust, omega)
                cars[i].calc_transelation(omega)
                cars[i].update_sensor_values(current_map)
                cars[i].read_goad_reached(goal_koord)
                cars[i].check_crash()
                outputs[i] = cars[i].brain.calculate_outputs(np.array([[cars[i].sensor_left_data[2]], [cars[i].sensor_left_up_data[2]], [cars[i].sensor_right_data[2]],[cars[i].sensor_right_up_data[2]], [cars[i].sensor_up_data[2]]]))

        #Updating the screen in 60 FPS
        for i in range(len(cars)):
            cars[i].rotate_car()
            cars[i].update_car()
            map.generation_control(generation)
        window.update()


        check = 0
        for i in range(len(cars)):
            if (cars[i].crash == True):
                check = check + 1

        if (check == len(cars)):
            dist = 0
            finished_cars = []
            for i in range(len(cars)):
                if (cars[i].finished == True):
                    finished_cars.append(cars[i])
                if (cars[i].distance > dist):
                    dist = cars[i].distance
                    new_brain1 = copy.copy(cars[i].brain)

                if (cars[i].distance > best_distance):
                    best_distance = cars[i].distance
                    new_brain = copy.copy(cars[i].brain)
                cars[i].delete_car()


            if (len(finished_cars) > 0):
                best_car = finished_cars[0]
                best_time = finished_cars[0].time

                for i in range(len(finished_cars)):
                    if (finished_cars[i].time < best_time):
                        best_car = finished_cars[i]
                        best_time = finished_cars[i].time

                new_brain = copy.copy(best_car.brain)
                new_brain1 = copy.copy(best_car.brain)

            cars.clear()
            new_generation = True
            generation = generation + 1


        while (time.time() - time_before) < period:
            time.sleep(0.00001)  # precision here


