import math
from math import pi as PI

def find_height(m):
    sum = 0
    for i in m:
        sum += i[11]
    return sum / len(m)

def mid_center(m):
    sum9 = 0
    sum10 = 0
    for i in m:
        sum9 += i[9]
        sum10 += i[10]
    return (sum9 / len(m), sum10 / len(m))

def eci_ro_euler(q1, q2, q3, q4):
    a = math.atan2 (2*(q1*q4+q2*q3),1-2*(q3*q3+q4*q4))
    b = math.asin (2*(q1*q3-q4*q2))
    c = math.atan2 (2*(q1*q2+q3*q4),1-2*(q2*q2+q3*q3))
    return a,b,c

'''def eci_ro_euler(q1, q2, q3, q4):
    a = math.atan2 (PI * (2*(q1*q4+q2*q3)) / 180, PI * (1-2*(q3*q3+q4*q4))/180)
    b = math.asin (PI * 2*(q1*q3-q4*q2) / 180)
    c = math.atan2 (PI * 2*(q1*q2+q3*q4)/ 180, PI * (1-2*(q2*q2+q3*q3)) / 180)
    return a,b,c'''

def to_time(mas):
    timemas = [31557600000000, 86400000000, 3600000000, 60000000, 1000000]
    datemas = []

    for i in mas:
        t = int(i[0])
        date = []
        for j in timemas:
            date.append(t // j)
            t %= j
        datemas.append(date)
    return datemas

def rotate_axis_z(q, points):
    newpoints = []
    for i in points:
        y,x = i
        newpoints.append((x*math.cos(q) + y * math.sin(q), -x*math.sin(q) + y*math.cos(q)))
    return newpoints

def see_obl(q,h):
    return 2 * h * (math.tan(PI * (q/2) / 180))

def get_movement_vetor(mas):
    return (mas[-1][9] - mas[0][9], mas[-1][10] - mas[0][10])
