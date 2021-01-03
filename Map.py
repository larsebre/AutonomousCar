from tkinter import *


class Map:

    def __init__(self, cvs):

        self.cvs = cvs
        self.gen = cvs.create_text(1300, 700,text = "Generation:      " + str(1), fill="darkblue",font="Times 20 italic bold")
        self.map_lines = []     #Koordinates
        self.lines = []         #Line objects
        self.starts = []
        self.goals = []
        """
        self.map_lines = [[(100, 750), (100, 400)], [(200, 750), (200, 450)], [(100, 400), (150, 320)], [(200, 450), (230, 400)], [(150, 320), (300, 320)],
                          [(230, 400), (320, 400)], [(300, 320), (300, 270)], [(320, 400), (420, 340)], [(420, 340), (420, 230)], [(300, 270), (220, 200)],
                          [(420, 230), (360, 200)], [(220, 200), (220, 90)], [(360, 200), (360, 120)], [(220, 90), (350, 10)], [(360, 120), (400, 80)],
                          [(350, 10), (1300, 10)], [(400, 80), (1250, 80)], [(1300, 10), (1400, 70)], [(1250, 80), (1320, 120)], [(1400, 70), (1400, 450)],
                          [(1320, 120), (1320, 400)], [(1400, 450), (1280, 520)], [(1320, 400), (1290, 420)], [(1280, 520), (800, 520)], [(1290, 420), (870, 420)],
                          [(800, 520), (750, 430)], [(870, 420), (810, 360)], [(750, 430), (600, 430)], [(810, 360), (500, 360)], [(600, 430), (600, 750)],
                          [(500, 360), (500, 750)]]
        """

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

