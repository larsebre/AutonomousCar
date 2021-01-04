from tkinter import *
import numpy as np
import math

def ccw(A,B,C):
	return (C[1]-A[1])*(B[0]-A[0]) > (B[1]-A[1])*(C[0]-A[0])

def intersect(A,B,C,D):
	return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

freq = 60.0

class Car:

    def __init__(self, x, y, cvs):
        self.cvs = cvs

        self.brain = None
        self.crash = False
        self.height = 50
        self.width = 25
        self.finished = False
        self.time = 0

        #Car
        self.body = np.array([[x, x + self.width, x + self.width, x],
                            [y, y, y - self.height, y - self.height]])                 #ld = left-down

        #Distance sensors
        self.sensors = np.array([[x, x - 90, x, x - 120, x + self.width, x + self.width + 90, x + self.width, x + self.width + 120, x + self.width/2.0, x + self.width/2.0],
                                     [y - 30, y - 30, y - 45, y - 200, y - 30, y - 30, y - 45, y - 200, y - self.height, y - self.height - 300]])


        """
        self.left = self.cvs.create_line(self.sensors[0][0], self.sensors[1][0], self.sensors[0][1], self.sensors[1][1])
        self.left_up = self.cvs.create_line(self.sensors[0][2], self.sensors[1][2], self.sensors[0][3], self.sensors[1][3])
        self.right = self.cvs.create_line(self.sensors[0][4], self.sensors[1][4], self.sensors[0][5], self.sensors[1][5])
        self.right_up = self.cvs.create_line(self.sensors[0][6], self.sensors[1][6], self.sensors[0][7], self.sensors[1][7])
        self.up = self.cvs.create_line(self.sensors[0][8], self.sensors[1][8], self.sensors[0][9], self.sensors[1][9])
        """


        self.sensor_left_data = [0, 0, 0]             #[min_x_val, min_y_val, distance]
        self.sensor_left_up_data = [0, 0, 0]
        self.sensor_right_data = [0, 0, 0]
        self.sensor_right_up_data = [0, 0, 0]
        self.sensor_up_data = [0, 0, 0]

        """
        self.left_cross = [self.cvs.create_line(self.sensor_left_data[0] - 3, self.sensor_left_data[1], self.sensor_left_data[0] + 3, self.sensor_left_data[1], fill = 'white'), self.cvs.create_line(self.sensor_left_data[0], self.sensor_left_data[1] - 3, self.sensor_left_data[0], self.sensor_left_data[1] + 3, fill = 'white')]
        self.left_up_cross = [self.cvs.create_line(self.sensor_left_up_data[0] - 3, self.sensor_left_up_data[1], self.sensor_left_up_data[0] + 3, self.sensor_left_up_data[1], fill = 'white'), self.cvs.create_line(self.sensor_left_up_data[0], self.sensor_left_up_data[1] - 3, self.sensor_left_up_data[0],self.sensor_left_up_data[1] + 3, fill = 'white')]
        self.right_cross = [self.cvs.create_line(self.sensor_right_data[0] - 3, self.sensor_right_data[1], self.sensor_right_data[0] + 3,self.sensor_right_data[1], fill = 'white'),self.cvs.create_line(self.sensor_right_data[0], self.sensor_right_data[1] - 3, self.sensor_right_data[0],self.sensor_right_data[1] + 3, fill = 'white')]
        self.right_up_cross = [self.cvs.create_line(self.sensor_right_up_data[0] - 3, self.sensor_right_up_data[1], self.sensor_right_up_data[0] + 3,self.sensor_right_up_data[1], fill = 'white'),self.cvs.create_line(self.sensor_right_up_data[0], self.sensor_right_up_data[1] - 3, self.sensor_right_up_data[0],self.sensor_right_up_data[1] + 3, fill = 'white')]
        self.up_cross = [self.cvs.create_line(self.sensor_up_data[0] - 3, self.sensor_up_data[1], self.sensor_up_data[0] + 3, self.sensor_up_data[1], fill = 'white'),self.cvs.create_line(self.sensor_up_data[0], self.sensor_up_data[1] - 3,self.sensor_up_data[0], self.sensor_up_data[1] + 3, fill = 'white')]
        """

        #Window
        self.w = np.array([[x + 2, x + self.width - 2, x + self.width - 2, x + 2],
                              [y - 35, y - 35, y - self.height, y - self.height]])  # ld = left-down

        self.color_glas = 'LightBlue3'
        self.color_car = 'red3'

        self.car = self.cvs.create_polygon(self.body[0][0], self.body[1][0],
                                           self.body[0][1], self.body[1][1],
                                           self.body[0][2], self.body[1][2],
                                           self.body[0][3], self.body[1][3],
                                           fill=self.color_car)
        self.wdw = self.cvs.create_polygon(self.w[0][0], self.w[1][0],
                                           self.w[0][1], self.w[1][1],
                                           self.w[0][2], self.w[1][2],
                                           self.w[0][3], self.w[1][3],
                                           fill=self.color_glas)


        #Physichal constants
        self.weight = 2000.0 #kg
        self.length = 4.98 #m
        self.d = 0.6 #m, 2.2
        self.k = 0.24  #Drag coefficient
        self.u_max = 11.98 * self.weight - 6000
        self.v_max = 69.4
        self.omega_max = 60 #Max degree of wheel angle. A bit unrealistic

        self.vel = 0.0
        self.vel_prev = 0.0
        self.distance = 0.0
        self.angle = 0.0
        self.angle_prev = 0.0
        self.angle_vel = 0.0
        self.angle_vel_prev = 0.0

        self.vel_x = 0.0
        self.vel_x_prev = 0.0
        self.vel_y = 0.0
        self.vel_y_prev = 0.0


    def update_car(self):
        self.cvs.delete(self.car)
        self.cvs.delete(self.wdw)

        """
        self.cvs.delete(self.left)
        self.cvs.delete(self.left_up)
        self.cvs.delete(self.right)
        self.cvs.delete(self.right_up)
        self.cvs.delete(self.up)

        self.cvs.delete(self.left_cross[0])
        self.cvs.delete(self.left_cross[1])
        self.cvs.delete(self.left_up_cross[0])
        self.cvs.delete(self.left_up_cross[1])
        self.cvs.delete(self.right_cross[0])
        self.cvs.delete(self.right_cross[1])
        self.cvs.delete(self.right_up_cross[0])
        self.cvs.delete(self.right_up_cross[1])
        self.cvs.delete(self.up_cross[0])
        self.cvs.delete(self.up_cross[1])
        """


        self.car = self.cvs.create_polygon(self.body[0][0], self.body[1][0],
                                           self.body[0][1], self.body[1][1],
                                           self.body[0][2], self.body[1][2],
                                           self.body[0][3], self.body[1][3],
                                           fill=self.color_car)
        self.wdw = self.cvs.create_polygon(self.w[0][0], self.w[1][0],
                                           self.w[0][1], self.w[1][1],
                                           self.w[0][2], self.w[1][2],
                                           self.w[0][3], self.w[1][3],
                                           fill=self.color_glas)
        """
        self.left = self.cvs.create_line(self.sensors[0][0], self.sensors[1][0], self.sensors[0][1], self.sensors[1][1])
        self.left_up = self.cvs.create_line(self.sensors[0][2], self.sensors[1][2], self.sensors[0][3],
                                            self.sensors[1][3])
        self.right = self.cvs.create_line(self.sensors[0][4], self.sensors[1][4], self.sensors[0][5],
                                          self.sensors[1][5])
        self.right_up = self.cvs.create_line(self.sensors[0][6], self.sensors[1][6], self.sensors[0][7],
                                             self.sensors[1][7])
        self.up = self.cvs.create_line(self.sensors[0][8], self.sensors[1][8], self.sensors[0][9], self.sensors[1][9])


        self.left_cross = [self.cvs.create_line(self.sensor_left_data[0] - 3, self.sensor_left_data[1], self.sensor_left_data[0] + 3,self.sensor_left_data[1], fill='white'),self.cvs.create_line(self.sensor_left_data[0], self.sensor_left_data[1] - 3, self.sensor_left_data[0],self.sensor_left_data[1] + 3, fill='white')]
        self.left_up_cross = [self.cvs.create_line(self.sensor_left_up_data[0] - 3, self.sensor_left_up_data[1],self.sensor_left_up_data[0] + 3, self.sensor_left_up_data[1],fill='white'),self.cvs.create_line(self.sensor_left_up_data[0], self.sensor_left_up_data[1] - 3,self.sensor_left_up_data[0], self.sensor_left_up_data[1] + 3,fill='white')]
        self.right_cross = [self.cvs.create_line(self.sensor_right_data[0] - 3, self.sensor_right_data[1],self.sensor_right_data[0] + 3, self.sensor_right_data[1],fill='white'),self.cvs.create_line(self.sensor_right_data[0], self.sensor_right_data[1] - 3,self.sensor_right_data[0], self.sensor_right_data[1] + 3,fill='white')]
        self.right_up_cross = [self.cvs.create_line(self.sensor_right_up_data[0] - 3, self.sensor_right_up_data[1],self.sensor_right_up_data[0] + 3, self.sensor_right_up_data[1],fill='white'),self.cvs.create_line(self.sensor_right_up_data[0], self.sensor_right_up_data[1] - 3,self.sensor_right_up_data[0], self.sensor_right_up_data[1] + 3,fill='white')]
        self.up_cross = [self.cvs.create_line(self.sensor_up_data[0] - 3, self.sensor_up_data[1], self.sensor_up_data[0] + 3,self.sensor_up_data[1], fill='white'),self.cvs.create_line(self.sensor_up_data[0], self.sensor_up_data[1] - 3, self.sensor_up_data[0],self.sensor_up_data[1] + 3, fill='white')]
        """

    def rotate_car(self):
        angle = self.angle - self.angle_prev
        self.angle_prev = self.angle
        center = np.matmul(self.body, np.array([[1], [1], [1], [1]])) / 4.0
        rotation_mat = np.array([[np.cos(np.pi * angle/180.0), np.sin(np.pi * angle/180.0)], [-np.sin(np.pi * angle/180.0), np.cos(np.pi * angle/180.0)]])

        self.body = np.matmul(rotation_mat, (self.body - center)) + center
        self.w = np.matmul(rotation_mat, (self.w - center)) + center

        self.sensors = np.matmul(rotation_mat, (self.sensors - center)) + center


    def calc_dynamics(self, thrust, omega):

        if (self.crash == False):
            # Here 1 m is 10 pixels, therefor multiplying with 10
            self.vel = np.exp(-self.k / (freq * self.weight)) * self.vel_prev + (1 / self.k) * (
                        1 - np.exp(-self.k / (freq * self.weight))) * thrust

            if (self.vel >= np.abs(self.v_max)):
                self.vel = self.vel_prev

            self.omega_max = 60 - (3/7.0) * abs(self.vel)               #To make it more realistic with reduced swing with high speeds

            self.distance = self.distance + (self.vel + self.vel_prev) * (1 / freq) * 0.5

            self.angle_vel = 10 * self.vel * (np.sin(np.pi * omega / 180.0)) / self.d
            self.angle = self.angle + (self.angle_vel + self.angle_vel_prev) * (1 / freq) * 0.5

            self.vel_prev = self.vel
            self.angle_vel_prev = self.angle_vel

        self.time = self.time + 1       #Keep track of time so that we can inherite from the fastes car
        if (self.time >= 800):
            self.crash = True

    def calc_transelation(self, omega):

        if (self.crash == False):
            ang = -(omega + self.angle)
            self.vel_x = self.vel * np.sin(np.pi * ang / 180.0)
            self.vel_y = self.vel * np.cos(np.pi * ang / 180.0)

            const = np.array([[((self.vel_x + self.vel_x_prev) * (1 / freq) * 0.5)], [-(self.vel_y + self.vel_y_prev) * (1 / freq) * 0.5]])
            self.body = self.body + 10 * np.array([[1, 1, 1, 1], [1, 1, 1, 1]]) * const
            self.w = self.w + 10 * np.array([[1, 1, 1, 1], [1, 1, 1, 1]]) * const
            self.sensors = self.sensors + 10 * np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]) * const

            self.vel_x_prev = self.vel_x
            self.vel_y_prev = self.vel_y

            self.rotate_car()

    def read_sensor_value(self, sensor, map):

        min_distance = 500
        min_x_val = 5000
        min_y_val = 5000

        for line in map:

            if (intersect(sensor[0], sensor[1], line[0], line[1])):

                denominator_1 = (sensor[1][0] - sensor[0][0])
                denominator_2 = (line[1][0] - line[0][0])
                if (denominator_1 == 0):
                    denominator_1 = 0.0000001
                if (denominator_2 == 0):
                    denominator_2 = 0.0000001

                x_val = (sensor[0][0] * (sensor[1][1] - sensor[0][1]) / (denominator_1) - sensor[0][1] - line[0][
                    0] * (line[1][1] - line[0][1]) / (denominator_2) + line[0][1]) / (
                                (sensor[1][1] - sensor[0][1]) / (denominator_1) - (line[1][1] - line[0][1]) / (
                            denominator_2))
                y_val = ((sensor[1][1] - sensor[0][1]) / (denominator_1)) * (x_val - sensor[0][0]) + sensor[0][1]

                if (math.isinf(x_val) or math.isinf(y_val)):
                    x_val = 5000
                    y_val = 5000

                x_val = math.floor(x_val)
                y_val = math.floor(y_val)

                distance = np.sqrt((sensor[0][1] - (y_val / 1.0)) ** 2 + (sensor[0][0] - (x_val / 1.0)) ** 2)  # [0]

                if (distance < min_distance):
                    min_distance = distance
                    min_x_val = x_val
                    min_y_val = y_val

        return min_x_val, min_y_val, min_distance


    def update_sensor_values(self, map):
        # Splitting the map up so that we dont have to iterate through all the lines to find the distance
        self.sensor_left_data = self.read_sensor_value([[self.sensors[0][0], self.sensors[1][0]], [self.sensors[0][1], self.sensors[1][1]]], map[0: math.floor(len(map)/2) + 1])
        self.sensor_left_up_data = self.read_sensor_value([[self.sensors[0][2], self.sensors[1][2]], [self.sensors[0][3], self.sensors[1][3]]], map[0: math.floor(len(map)/2) + 1])
        self.sensor_right_data = self.read_sensor_value([[self.sensors[0][4], self.sensors[1][4]], [self.sensors[0][5], self.sensors[1][5]]], map[math.floor(len(map)/2) - 1: -1])
        self.sensor_right_up_data = self.read_sensor_value([[self.sensors[0][6], self.sensors[1][6]], [self.sensors[0][7], self.sensors[1][7]]], map[math.floor(len(map)/2) - 1: -1])
        self.sensor_up_data = self.read_sensor_value([[self.sensors[0][8], self.sensors[1][8]], [self.sensors[0][9], self.sensors[1][9]]], map)


    def check_crash(self):
        crash_distance = 6
        if ((self.sensor_left_data[2] <= crash_distance) or (self.sensor_left_up_data[2] <= crash_distance) or (self.sensor_right_data[2] <= crash_distance) or (self.sensor_right_up_data[2] <= crash_distance) or (self.sensor_up_data[2] <= crash_distance)):
            self.crash = True
            self.vel = 0

    def read_goad_reached(self, goal_koord):

        line = [[(goal_koord[0] - 70, goal_koord[1]), (goal_koord[0] + 70, goal_koord[1])]]

        data = self.read_sensor_value([[self.sensors[0][8], self.sensors[1][8]], [self.sensors[0][9], self.sensors[1][9]]], line)   #checking just for the up sensor
        if (data[2] <= 10):
            self.finished = True
            self.crash = True


    def delete_car(self):
        self.cvs.delete(self.car)
        self.cvs.delete(self.wdw)

        """
        self.cvs.delete(self.left)
        self.cvs.delete(self.left_up)
        self.cvs.delete(self.right)
        self.cvs.delete(self.right_up)
        self.cvs.delete(self.up)

        self.cvs.delete(self.left_cross[0])
        self.cvs.delete(self.left_cross[1])
        self.cvs.delete(self.left_up_cross[0])
        self.cvs.delete(self.left_up_cross[1])
        self.cvs.delete(self.right_cross[0])
        self.cvs.delete(self.right_cross[1])
        self.cvs.delete(self.right_up_cross[0])
        self.cvs.delete(self.right_up_cross[1])
        self.cvs.delete(self.up_cross[0])
        self.cvs.delete(self.up_cross[1])
        """

