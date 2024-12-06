import numpy as np
from decimal import Decimal
import csv
import math

def quaternion_to_rotation_matrix(q):
    w, x, y, z = q
    return np.array([
        [1 - 2*(y**2 + z**2), 2*(x*y - w*z), 2*(x*z + w*y)],
        [2*(x*y + w*z), 1 - 2*(x**2 + z**2), 2*(y*z - w*x)],
        [2*(x*z - w*y), 2*(y*z + w*x), 1 - 2*(x**2 + y**2)]
    ])

def rotation_matrix_to_euler(R):
    yaw = np.arctan2(R[1, 0], R[0, 0])  
    pitch = np.arcsin(-R[2, 0])         
    roll = np.arctan2(R[2, 1], R[2, 2]) 
    return np.degrees(yaw), np.degrees(pitch), np.degrees(roll)


#######################################################

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!УСРЕДНЯТЬ ЗНАЧЕНИЯ!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def get_rotation_matrix(file = 'logs/beacon_human.csv'):
    mas = []

    with open(file, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            if row != [] and row[0] != 'time usec':
                l = []
                for i in row:
                    n = float(i)
                    l.append(n)
                mas.append(l)
    c = []
    for i in mas:
        f = [i[1], i[2], i[3], i[4]]
        f = quaternion_to_rotation_matrix(f)
        f = rotation_matrix_to_euler(f)
        c.append(f)
    return c

 