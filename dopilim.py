import newmath
import to_geojs as tgjs
import math
from math import pi as PI
import os
import csv
import newhtml

img = 'pic3/2024-10-24_09-23-56_SXC3-227_1.jpg'
vert = 62.2
gor = 48.8

def quat_to_eul_mas(m):
    mas = []
    for i in m:
        mas.append((newmath.eci_ro_euler(i[5],i[6],i[7],i[8])))
    return mas

def get_movement_vetor(mas):
    return (mas[-1][9] - mas[0][9], mas[-1][10] - mas[0][10])

dirs = os.listdir('pic3')

f = -1
for i in dirs:
    c = i.find('.jpg')
    if c != -1:
        fototime = int(i[17:19])
        break
c = fototime

mas = []

with open('pic3/logs/beacon_human.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        if row != [] and row[0] != 'time usec':
            l = []
            for i in row:
                n = float(i)
                l.append(n)
            mas.append(l)


h = newmath.find_height(mas)
euler_mas = quat_to_eul_mas(mas)

mov_vector = get_movement_vetor(mas)

print(mov_vector)



