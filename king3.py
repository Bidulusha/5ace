from ace4 import get_rotation_matrix
import newmath
import math
from math import pi as PI
import csv


def quat_to_eul_mas(m):
    mas = []
    for i in m:
        mas.append((newmath.eci_ro_euler(i[5],i[6],i[7],i[8])))
    return mas

vert = 62.2
gor = 48.8


#matrix = get_rotation_matrix()

mas = []

with open('logs/beacon_human.csv', newline='') as csvfile:
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

for i in euler_mas:
    print(i)

'''
for i in matrix:
    print(i)

'''


for i in euler_mas:
    bigv = math.tan(PI * (i[0] + vert / 2) / 180) * h / 1000
    smalv = math.tan(PI * (i[0] - vert / 2) / 180) * h / 1000

    bigg = math.tan(PI * (i[1] + vert / 2) / 180) * h / 1000
    smalg = math.tan(PI * (i[1] - vert / 2) / 180) * h / 1000


grad = 360 / 40000

l = [mas[0][9] + bigv * grad ,mas[0][9] + smalv * grad]
f = [mas[0][10] + bigg * grad, mas[0][10] + smalg * grad]

#print(a)