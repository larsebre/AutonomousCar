from tkinter import *


class Map:

    def __init__(self, cvs):

        self.cvs = cvs
        self.gen = cvs.create_text(1300, 700,text = "Generation:      " + str(1), fill="darkblue",font="Times 20 italic bold")
        self.map_lines = []     #Koordinates
        self.lines = []         #Line objects
        self.starts = []
        self.goals = []


    def print_map(self, index):

        for line in self.map_lines[index]:

            l = self.cvs.create_line(line[0][0], line[0][1], line[1][0], line[1][1], width = 3)
            self.lines.append(l)

        l = self.cvs.create_line(self.goals[index][0] - 70, self.goals[index][1], self.goals[index][0] + 70, self.goals[index][1], width = 5, fill = 'green')
        self.lines.append(l)


    def erase_map(self):

        for line in self.lines:
           self.cvs.delete(line)

        self.lines.clear()

    def generation_control(self, num):

        self.cvs.delete(self.gen)
        self.gen = self.cvs.create_text(1300, 700,text = "Generation:      " + str(num), fill="darkblue",font="Times 20 italic bold")


    def load_maps(self, path):
        file = open(path, "r")
        Lines = file.readlines()

        for line in Lines:
            line = line.split("-")
            temp_list = []
            for x in line:
                x = x.split('|')
                x[0] = x[0].split(',')
                x[1] = x[1].split(',')

                tup1 = (int(x[0][0]), int(x[0][1]))
                tup2 = (int(x[1][0]), int(x[1][1]))

                temp_list.append([tup1, tup2])

            self.starts.append(temp_list[-1][0])
            self.goals.append(temp_list[-1][1])
            temp_list.pop(-1)
            self.map_lines.append(temp_list)

        file.close()

