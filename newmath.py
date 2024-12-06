import math

def find_height(m):
    sum = 0
    for i in m:
        sum += i[11]
    return sum / len(m)

def eci_ro_euler(q1, q2, q3, q4):
    a = math.atan2 (2*(q1*q4+q2*q3),1-2*(q3*q3+q4*q4))
    b = math.asin (2*(q1*q3-q4*q2))
    c = math.atan2 (2*(q1*q2+q3*q4),1-2*(q2*q2+q3*q3))
    return a,b,c

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
        x,y = i
        newpoints.append((x*math.cos(q) + y * math.sin(q), -x*math.sin(q) + y*math.cos(q)))
    return newpoints
