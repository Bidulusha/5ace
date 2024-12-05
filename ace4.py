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

def euler_to_rotation_matrix(yaw, pitch, roll):
    """Создаёт матрицу вращения из углов Yaw, Pitch, Roll."""
    yaw = np.radians(yaw)
    pitch = np.radians(pitch)
    roll = np.radians(roll)

    R_yaw = np.array([
        [np.cos(yaw), -np.sin(yaw), 0],
        [np.sin(yaw),  np.cos(yaw), 0],
        [0,            0,           1]
    ])

    R_pitch = np.array([
        [np.cos(pitch), 0, np.sin(pitch)],
        [0,             1, 0],
        [-np.sin(pitch), 0, np.cos(pitch)]
    ])

    R_roll = np.array([
        [1, 0,           0],
        [0, np.cos(roll), -np.sin(roll)],
        [0, np.sin(roll),  np.cos(roll)]
    ])

    return R_yaw @ R_pitch @ R_roll

def eci_to_orb_matrix(r, v):
    """Вычисляет матрицу перехода из ECI в ORB."""
    z_orb = -r / np.linalg.norm(r)  # Надир
    h = np.cross(r, v)  # Орбитальный момент
    y_orb = h / np.linalg.norm(h)  # Нормаль к орбите
    x_orb = np.cross(y_orb, z_orb)  # Орбитальное движение
    return np.vstack([x_orb, y_orb, z_orb]).T

def rotation_matrix_to_euler_eci(R):
    """Извлекает углы Yaw, Pitch, Roll из матрицы вращения."""
    pitch = np.arcsin(-R[2, 0])  # Из-за особого поведения sin
    yaw = np.arctan2(R[1, 0], R[0, 0])
    roll = np.arctan2(R[2, 1], R[2, 2])
    return np.degrees(yaw), np.degrees(pitch), np.degrees(roll)

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

    # Пример положения и скорости аппарата в системе ECI (в км и км/с)
    r = np.array([6378.1 + mas[0][11], 0, 0])  # Вектор положения
    v = np.array([0, math.sqrt(398600 / r[0]), 0])  # Вектор скорости

    cc = []
    for i in c:
    # Матрица вращения из ECI углов
        R_eci = euler_to_rotation_matrix(i[0], i[1], i[2])
        # Матрица перехода из ECI в ORB
        T_eci_to_orb = eci_to_orb_matrix(r, v)
        # Преобразование матрицы вращения в ORB
        R_orb = T_eci_to_orb @ R_eci
        cc.append(R_orb)

    orb_matrix = []
    for i in cc:
        # Извлечение углов Yaw, Pitch, Roll в системе ORB
        yaw_orb, pitch_orb, roll_orb = rotation_matrix_to_euler_eci(i)
        orb_matrix.append([yaw_orb, pitch_orb, roll_orb])
    return orb_matrix



