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


##################################GET FotoTime##################################
dirs = os.listdir('pic3')

f = -1
for i in dirs:
    c = i.find('.jpg')
    if c != -1:
        fototime = int(i[17:19])
        break
c = fototime
##################################GET FotoTime##################################


##################################GET MAS##################################
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
##################################GET MAS##################################

##################################GET time from FotoTime##################################
datetime = newmath.to_time(mas)
tt = set()
for i in range(1,len(datetime) - 1):
    if datetime[i][-1] == c or datetime[i][-1] > c and datetime[i - 1][-1] < c:
        tt.add(i - 1)
        tt.add(i)
        tt.add(i + 1)

tt = sorted(tt)
##################################GET time from FotoTime##################################

##################################Loot indexis that we need##################################
a, b = tt[len(tt) % 2 ], tt[len(tt) % 2 + 1]

euler_index = list((euler_mas[a][i] + euler_mas[b][i]) / 2 for i in range(3))
mv = newmath.get_movement_vetor(mas)

'''euler_index[0] *= mv[0] / abs(mv[0])
euler_index[1] *= mv[1] / abs(mv[1])'''
zn = (mv[0] / abs(mv[0]), mv[1] / abs(mv[1]))
##################################Loot indexis that we need##################################

##################################GET new latitude and longtitude##################################

vertd = newmath.see_obl(vert, mas[a][11] / 1000) / 2
gord = newmath.see_obl(gor, mas[a][11] / 1000) / 2
#############Нужно ли учитывать поворот камеры или нет?
#c = (mas[a][9], mas[a][10])
c = newmath.mid_center(mas)
print(euler_index)
#c = ((c[0] + mas[a][11] * math.tan(PI * (gor / 2 + euler_index[0]) / 180) / 111230), (c[1] + mas[a][11] * math.tan(PI * (vert / 2 + euler_index[1]) / 180)/ (111230 * math.cos(c[0]))))

cc = ((c[1] + vertd / (111.23 * math.cos(PI * c[0] / 180)), c[1] - vertd / (111.23 * math.cos(PI * c[0] / 180))), 
      (c[0] + gord / 111.23, c[0] - gord / (111.23)))
print(c)
print(cc)

print(vertd, gord)
##################################GET new latitude and longtitude##################################

##################################GEO##################################
points = [
    (cc[1][0], cc[0][0]), (cc[1][0], cc[0][1]),
    (cc[1][1], cc[0][0]), (cc[1][1], cc[0][1]),
]
newpoints = newmath.rotate_axis_z(abs(euler_index[2]), points)
print(points, end ='\n\n')
print(newpoints)

tgjs.create_geojson_with_image(img, points)
newhtml.create_html_file(img)
