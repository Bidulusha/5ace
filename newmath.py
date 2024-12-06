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
