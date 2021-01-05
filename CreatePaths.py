from tkinter import *
import sys


sys.setswitchinterval(100)

window = Tk()
canvas_width = 2000
canvas_height = 1000

width_track = 100

cvs = Canvas(window, height=canvas_height, width=canvas_width, bg = 'light grey')
cvs.pack()

prev_points = [0,0]
start_koord = [0,0]
goal_koord = [0,0]

new_line1 = cvs.create_line(prev_points[0], prev_points[1], 0, 0)
map = []

def show_lines(event, arg):
    x = event.x
    y = event.y

    cvs.delete(arg[0])

    arg[0] = cvs.create_line(arg[1][0], arg[1][1], x, y, fill = 'green')

start = False
def set_lines(event, arg):
    x = event.x
    y = event.y

    if (arg[2] == False):
        arg[0] = [x, y]
        arg[2] = True
    else:
        cvs.bind('<Motion>', lambda event, arg=[new_line1, arg[0]]: show_lines(event, arg))
        arg[1].append([(arg[0][0], arg[0][1]), (x, y)])

        cvs.create_line(arg[0][0], arg[0][1], x, y)
        prev_points = [x, y]
        arg[0][0] = x
        arg[0][1] = y



def write_to_file(start_koord, goal_koord):

    file = open('.../CarTracks.txt', "a")
    for i in range(len(map)):
        file.write(str(map[i][0][0]) + ',' +  str(map[i][0][1]) + '|' +  str(map[i][1][0]) + ',' + str(map[i][1][1]))
        file.write('-')

    file.write(str(start_koord[0]) + ',' + str(start_koord[1]) + '|' + str(goal_koord[0]) + ',' + str(goal_koord[1]))
    file.write('\n')
    file.close()

counter = 0
def set_start_and_goal(event, arg):
    koord = [event.x, event.y]

    if (arg[2] == 0):
        arg[0] = koord
        cvs.create_rectangle(arg[0][0], arg[0][1], arg[0][0] + 10, arg[0][1] + 10)
    elif (arg[2] == 1):
        arg[1] = koord
        cvs.create_rectangle(arg[1][0], arg[1][1], arg[1][0] + 10, arg[1][1] + 10, fill='green')
    else:
        write_to_file(arg[0], arg[1])

    arg[2] = arg[2] + 1

cvs.bind('<Button-1>', lambda event, arg = [prev_points, map, start]: set_lines(event, arg))
cvs.bind('<Double-Button-2>', lambda event, arg = [start_koord, goal_koord, counter]: set_start_and_goal(event, arg))

while True:
    cvs.update()
