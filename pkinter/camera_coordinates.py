#import to_geojs as tgjs
import newmath
from . import newhtml
import math
from math import pi as PI
import os
import csv

'''vert = 62.2
gor = 48.8'''

vert = 48.8
gor = 62.2

def looting(img, filecsv):
    def quat_to_eul_mas(m):
        mas = []
        for i in m:
            mas.append((newmath.eci_ro_euler(i[5],i[6],i[7],i[8])))
        return mas


    ##################################GET FotoTime##################################
    i = os.path.basename(img)
    c = int(i[17:19])

    ##################################GET FotoTime##################################


    ##################################GET MAS##################################
    mas = []
    with open(filecsv, newline='') as csvfile:
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

    #for i in euler_mas:
        #print(i)

    a, b = tt[len(tt) % 2 ], tt[len(tt) % 2 + 1]
    euler_index = list((euler_mas[a][i] + euler_mas[b][i]) / 2 for i in range(3))

    ##################################Loot indexis that we need##################################

    ##################################GET new latitude and longtitude##################################


    bigv = math.tan(PI * (euler_index[0] + vert / 2) / 180) * h / 1000
    smalv = math.tan(PI * (euler_index[0] - vert / 2) / 180) * h / 1000

    bigg = math.tan(PI * (euler_index[1] + gor / 2) / 180) * h / 1000
    smalg = math.tan(PI * (euler_index[1] - gor / 2) / 180) * h / 1000


    grad = 360 / 40000

    l = (mas[a][9] + mas[b][9]) / 2
    ll = (mas[a][10] + mas[b][10]) / 2

    latit = ((mas[0][9] + bigg * grad,  ll), (mas[0][9] + smalg * grad, ll))
    long = ((l, mas[0][10] + bigv * grad), (l, mas[0][10] + smalv * grad))

    #print(l, ', ', ll)
    #print(latit)
    #print(long)
    points = ((latit[0][0], long[0][1]),(latit[0][0], long[1][1]),(latit[1][0], long[0][1]),(latit[1][0], long[1][1]))
    newpoints = newmath.rotate_axis_z((PI * euler_index[2])/180, points)
    #for i in points:
        #print(i)
    #print()
    #for i in newpoints:
        #print(i)
    ##################################GET new latitude and longtitude##################################
    newhtml.create_html_file()
    tgjs.create_geojson_with_image(img, points)
    return points
    ##################################GEO##################################

    #tgjs.create_geojson_with_image(img, newpoints)