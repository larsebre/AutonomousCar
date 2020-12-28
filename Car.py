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

        #Car
        self.ld = np.array([[x], [y]])                 #ld = left-down
        self.rd = np.array([[x + self.width], [y]])
        self.lu = np.array([[x], [y - self.height]])
        self.ru = np.array([[x + self.width], [y - self.height]])

        #Distance sensors
        self.sensor_left = [np.array([[x], [y - 30]]), np.array([[x - 90], [y - 30]])]
        self.sensor_left_up = [np.array([[x], [y - 45]]), np.array([[x - 120], [y - 200]])]
        self.sensor_right = [np.array([[x + self.width], [y - 30]]), np.array([[x + self.width + 90], [y - 30]])]
        self.sensor_right_up = [np.array([[x + self.width], [y - 45]]), np.array([[x + self.width + 120], [y - 200]])]
        self.sensor_up = [np.array([[x + self.width/2.0], [y - self.height]]), np.array([[x + self.width/2.0], [y - self.height - 300]])]

        """
        self.left = self.cvs.create_line(self.sensor_left[0][0][0], self.sensor_left[0][1][0], self.sensor_left[1][0][0], self.sensor_left[1][1][0])
        self.left_up = self.cvs.create_line(self.sensor_left_up[0][0][0], self.sensor_left_up[0][1][0], self.sensor_left_up[1][0][0], self.sensor_left_up[1][1][0])
        self.right = self.cvs.create_line(self.sensor_right[0][0][0], self.sensor_right[0][1][0], self.sensor_right[1][0][0], self.sensor_right[1][1][0])
        self.right_up = self.cvs.create_line(self.sensor_right_up[0][0][0], self.sensor_right_up[0][1][0], self.sensor_right_up[1][0][0], self.sensor_right_up[1][1][0])
        self.up = self.cvs.create_line(self.sensor_up[0][0][0], self.sensor_up[0][1][0], self.sensor_up[1][0][0], self.sensor_up[1][1][0])
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
        self.ld_w = np.array([[x + 2], [y - 35]])  # ld = left-down
        self.rd_w = np.array([[x + self.width - 2], [y - 35]])
        self.lu_w = np.array([[x + 2], [y - self.height]])
        self.ru_w = np.array([[x + self.width - 2], [y - self.height]])

        self.color_glas = 'LightBlue3'
        self.color_car = 'red3'

        self.car = self.cvs.create_polygon(self.ld[0][0], self.ld[1][0], self.rd[0][0], self.rd[1][0], self.ru[0][0],
                                       self.ru[1][0], self.lu[0][0], self.lu[1][0], fill=self.color_car)
        self.wdw = self.cvs.create_polygon(self.ld_w[0][0], self.ld_w[1][0], self.rd_w[0][0], self.rd_w[1][0],
                                       self.ru_w[0][0], self.ru_w[1][0], self.lu_w[0][0], self.lu_w[1][0],
                                       fill=self.color_glas)


        #Physichal constants
        self.weight = 2000.0 #kg
        self.length = 4.98 #m
        self.d = 0.6 #m, 2.2
        self.k = 0.24  #Drag coefficient
        self.u_max = 11.98 * self.weight
        self.v_max = 69.4
        self.omega_max = 60 #Max degree of wheel angle

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
        """
        """
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

        self.car = self.cvs.create_polygon(self.ld[0][0], self.ld[1][0], self.rd[0][0], self.rd[1][0], self.ru[0][0], self.ru[1][0], self.lu[0][0], self.lu[1][0], fill = self.color_car)
        self.wdw = self.cvs.create_polygon(self.ld_w[0][0], self.ld_w[1][0], self.rd_w[0][0], self.rd_w[1][0], self.ru_w[0][0], self.ru_w[1][0], self.lu_w[0][0], self.lu_w[1][0], fill=self.color_glas)

        """
        self.left = self.cvs.create_line(self.sensor_left[0][0][0], self.sensor_left[0][1][0],self.sensor_left[1][0][0], self.sensor_left[1][1][0])
        self.left_up = self.cvs.create_line(self.sensor_left_up[0][0][0], self.sensor_left_up[0][1][0],self.sensor_left_up[1][0][0], self.sensor_left_up[1][1][0])
        self.right = self.cvs.create_line(self.sensor_right[0][0][0], self.sensor_right[0][1][0],self.sensor_right[1][0][0], self.sensor_right[1][1][0])
        self.right_up = self.cvs.create_line(self.sensor_right_up[0][0][0], self.sensor_right_up[0][1][0],self.sensor_right_up[1][0][0], self.sensor_right_up[1][1][0])
        self.up = self.cvs.create_line(self.sensor_up[0][0][0], self.sensor_up[0][1][0], self.sensor_up[1][0][0],self.sensor_up[1][1][0])
        """
        """
        self.left_cross = [self.cvs.create_line(self.sensor_left_data[0] - 3, self.sensor_left_data[1], self.sensor_left_data[0] + 3,self.sensor_left_data[1], fill='white'),self.cvs.create_line(self.sensor_left_data[0], self.sensor_left_data[1] - 3, self.sensor_left_data[0],self.sensor_left_data[1] + 3, fill='white')]
        self.left_up_cross = [self.cvs.create_line(self.sensor_left_up_data[0] - 3, self.sensor_left_up_data[1],self.sensor_left_up_data[0] + 3, self.sensor_left_up_data[1],fill='white'),self.cvs.create_line(self.sensor_left_up_data[0], self.sensor_left_up_data[1] - 3,self.sensor_left_up_data[0], self.sensor_left_up_data[1] + 3,fill='white')]
        self.right_cross = [self.cvs.create_line(self.sensor_right_data[0] - 3, self.sensor_right_data[1],self.sensor_right_data[0] + 3, self.sensor_right_data[1],fill='white'),self.cvs.create_line(self.sensor_right_data[0], self.sensor_right_data[1] - 3,self.sensor_right_data[0], self.sensor_right_data[1] + 3,fill='white')]
        self.right_up_cross = [self.cvs.create_line(self.sensor_right_up_data[0] - 3, self.sensor_right_up_data[1],self.sensor_right_up_data[0] + 3, self.sensor_right_up_data[1],fill='white'),self.cvs.create_line(self.sensor_right_up_data[0], self.sensor_right_up_data[1] - 3,self.sensor_right_up_data[0], self.sensor_right_up_data[1] + 3,fill='white')]
        self.up_cross = [self.cvs.create_line(self.sensor_up_data[0] - 3, self.sensor_up_data[1], self.sensor_up_data[0] + 3,self.sensor_up_data[1], fill='white'),self.cvs.create_line(self.sensor_up_data[0], self.sensor_up_data[1] - 3, self.sensor_up_data[0],self.sensor_up_data[1] + 3, fill='white')]
        """

    def rotate_car(self):
        angle = self.angle - self.angle_prev
        self.angle_prev = self.angle
        center = (self.ld + self.rd + self.lu + self.ru)/4.0
        rotation_mat = np.array([[np.cos(np.pi * angle/180.0), np.sin(np.pi * angle/180.0)], [-np.sin(np.pi * angle/180.0), np.cos(np.pi * angle/180.0)]])
        self.ld = np.matmul(rotation_mat, (self.ld - center)) + center
        self.rd = np.matmul(rotation_mat, (self.rd - center)) + center
        self.lu = np.matmul(rotation_mat, (self.lu - center)) + center
        self.ru = np.matmul(rotation_mat, (self.ru - center)) + center
        self.ld_w = np.matmul(rotation_mat, (self.ld_w - center)) + center
        self.rd_w = np.matmul(rotation_mat, (self.rd_w - center)) + center
        self.lu_w = np.matmul(rotation_mat, (self.lu_w - center)) + center
        self.ru_w = np.matmul(rotation_mat, (self.ru_w - center)) + center

        self.sensor_left = [np.matmul(rotation_mat, (self.sensor_left[0] - center)) + center, np.matmul(rotation_mat, (self.sensor_left[1] - center)) + center]
        self.sensor_left_up = [np.matmul(rotation_mat, (self.sensor_left_up[0] - center)) + center, np.matmul(rotation_mat, (self.sensor_left_up[1] - center)) + center]
        self.sensor_right = [np.matmul(rotation_mat, (self.sensor_right[0] - center)) + center, np.matmul(rotation_mat, (self.sensor_right[1] - center)) + center]
        self.sensor_right_up = [np.matmul(rotation_mat, (self.sensor_right_up[0] - center)) + center, np.matmul(rotation_mat, (self.sensor_right_up[1] - center)) + center]
        self.sensor_up = [np.matmul(rotation_mat, (self.sensor_up[0] - center)) + center, np.matmul(rotation_mat, (self.sensor_up[1] - center)) + center]


    def calc_dynamics(self, thrust, omega):

        if (self.crash == False):
            # Here 1 m is 10 pixels, therefor multiplying with 10
            self.vel = np.exp(-self.k / (freq * self.weight)) * self.vel_prev + (1 / self.k) * (
                        1 - np.exp(-self.k / (freq * self.weight))) * thrust

            if (self.vel >= np.abs(self.v_max)):
                self.vel = self.vel_prev

            self.distance = self.distance + (self.vel + self.vel_prev) * (1 / freq) * 0.5

            self.angle_vel = 10 * self.vel * (np.sin(np.pi * omega / 180.0)) / self.d
            self.angle = self.angle + (self.angle_vel + self.angle_vel_prev) * (1 / freq) * 0.5

            self.vel_prev = self.vel
            self.angle_vel_prev = self.angle_vel


    def calc_transelation(self, omega):

        if (self.crash == False):
            ang = -(omega + self.angle)
            self.vel_x = self.vel * np.sin(np.pi * ang / 180.0)
            self.vel_y = self.vel * np.cos(np.pi * ang / 180.0)

            self.ld = self.ld + 10 * np.array([[(self.vel_x + self.vel_x_prev) * (1 / freq) * 0.5],
                                               [-(self.vel_y + self.vel_y_prev) * (1 / freq) * 0.5]])
            self.rd = self.rd + 10 * np.array([[(self.vel_x + self.vel_x_prev) * (1 / freq) * 0.5],
                                               [-(self.vel_y + self.vel_y_prev) * (1 / freq) * 0.5]])
            self.lu = self.lu + 10 * np.array([[(self.vel_x + self.vel_x_prev) * (1 / freq) * 0.5],
                                               [-(self.vel_y + self.vel_y_prev) * (1 / freq) * 0.5]])
            self.ru = self.ru + 10 * np.array([[(self.vel_x + self.vel_x_prev) * (1 / freq) * 0.5],
                                               [-(self.vel_y + self.vel_y_prev) * (1 / freq) * 0.5]])
            self.ld_w = self.ld_w + 10 * np.array([[(self.vel_x + self.vel_x_prev) * (1 / freq) * 0.5],
                                                   [-(self.vel_y + self.vel_y_prev) * (1 / freq) * 0.5]])
            self.rd_w = self.rd_w + 10 * np.array([[(self.vel_x + self.vel_x_prev) * (1 / freq) * 0.5],
                                                   [-(self.vel_y + self.vel_y_prev) * (1 / freq) * 0.5]])
            self.lu_w = self.lu_w + 10 * np.array([[(self.vel_x + self.vel_x_prev) * (1 / freq) * 0.5],
                                                   [-(self.vel_y + self.vel_y_prev) * (1 / freq) * 0.5]])
            self.ru_w = self.ru_w + 10 * np.array([[(self.vel_x + self.vel_x_prev) * (1 / freq) * 0.5],
                                                   [-(self.vel_y + self.vel_y_prev) * (1 / freq) * 0.5]])

            self.sensor_left = [self.sensor_left[0] + 10 * np.array(
                [[(self.vel_x + self.vel_x_prev) * (1 / freq) * 0.5],
                 [-(self.vel_y + self.vel_y_prev) * (1 / freq) * 0.5]]),
                                self.sensor_left[1] + 10 * np.array(
                                    [[(self.vel_x + self.vel_x_prev) * (1 / freq) * 0.5],
                                     [-(self.vel_y + self.vel_y_prev) * (1 / freq) * 0.5]])]

            self.sensor_left_up = [self.sensor_left_up[0] + 10 * np.array(
                [[(self.vel_x + self.vel_x_prev) * (1 / freq) * 0.5],
                 [-(self.vel_y + self.vel_y_prev) * (1 / freq) * 0.5]]),
                                   self.sensor_left_up[1] + 10 * np.array(
                                       [[(self.vel_x + self.vel_x_prev) * (1 / freq) * 0.5],
                                        [-(self.vel_y + self.vel_y_prev) * (1 / freq) * 0.5]])]

            self.sensor_right = [self.sensor_right[0] + 10 * np.array(
                [[(self.vel_x + self.vel_x_prev) * (1 / freq) * 0.5],
                 [-(self.vel_y + self.vel_y_prev) * (1 / freq) * 0.5]]),
                                 self.sensor_right[1] + 10 * np.array(
                                     [[(self.vel_x + self.vel_x_prev) * (1 / freq) * 0.5],
                                      [-(self.vel_y + self.vel_y_prev) * (1 / freq) * 0.5]])]

            self.sensor_right_up = [self.sensor_right_up[0] + 10 * np.array(
                [[(self.vel_x + self.vel_x_prev) * (1 / freq) * 0.5],
                 [-(self.vel_y + self.vel_y_prev) * (1 / freq) * 0.5]]),
                                    self.sensor_right_up[1] + 10 * np.array(
                                        [[(self.vel_x + self.vel_x_prev) * (1 / freq) * 0.5],
                                         [-(self.vel_y + self.vel_y_prev) * (1 / freq) * 0.5]])]

            self.sensor_up = [self.sensor_up[0] + 10 * np.array([[(self.vel_x + self.vel_x_prev) * (1 / freq) * 0.5], [
                -(self.vel_y + self.vel_y_prev) * (1 / freq) * 0.5]]),
                              self.sensor_up[1] + 10 * np.array([[(self.vel_x + self.vel_x_prev) * (1 / freq) * 0.5], [
                                  -(self.vel_y + self.vel_y_prev) * (1 / freq) * 0.5]])]

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

                x_val = (sensor[0][0] * (sensor[1][1] - sensor[0][1]) / (denominator_1) - sensor[0][1] - line[0][0] * (
                            line[1][1] - line[0][1]) / (denominator_2) + line[0][1]) / (
                                    (sensor[1][1] - sensor[0][1]) / (denominator_1) - (line[1][1] - line[0][1]) / (
                                denominator_2))
                y_val = ((sensor[1][1] - sensor[0][1]) / (denominator_1)) * (x_val - sensor[0][0]) + sensor[0][1]

                if (math.isinf(x_val) or math.isinf(y_val)):
                    x_val = 5000
                    y_val = 5000

                x_val = math.floor(x_val)
                y_val = math.floor(y_val)

                distance = np.sqrt((sensor[0][1] - (y_val / 1.0)) ** 2 + (sensor[0][0] - (x_val / 1.0)) ** 2)[0]

                if (distance < min_distance):
                    min_distance = distance
                    min_x_val = x_val
                    min_y_val = y_val


        return min_x_val, min_y_val, min_distance


    def update_sensor_values(self, map):
        self.sensor_left_data = self.read_sensor_value(self.sensor_left, map)
        self.sensor_left_up_data = self.read_sensor_value(self.sensor_left_up, map)
        self.sensor_right_data = self.read_sensor_value(self.sensor_right, map)
        self.sensor_right_up_data = self.read_sensor_value(self.sensor_right_up, map)
        self.sensor_up_data = self.read_sensor_value(self.sensor_up, map)

    def check_crash(self):
        crash_distance = 5
        if ((self.sensor_left_data[2] <= crash_distance) or (self.sensor_left_up_data[2] <= crash_distance) or (self.sensor_right_data[2] <= crash_distance) or (self.sensor_right_up_data[2] <= crash_distance) or (self.sensor_up_data[2] <= crash_distance)):
            self.crash = True
            self.vel = 0



    def delete_car(self):
        self.cvs.delete(self.car)
        self.cvs.delete(self.wdw)
        """
        self.cvs.delete(self.left)
        self.cvs.delete(self.left_up)
        self.cvs.delete(self.right)
        self.cvs.delete(self.right_up)
        self.cvs.delete(self.up)
        """

        """
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
