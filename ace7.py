import numpy as np
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
    pitch = np.arcsin(-R[2, 0])
    yaw = np.arctan2(R[1, 0], R[0, 0])
    roll = np.arctan2(R[2, 1], R[2, 2])
    return np.degrees(yaw), np.degrees(pitch), np.degrees(roll)

def euler_to_rotation_matrix(yaw, pitch, roll):
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
    z_orb = -r / np.linalg.norm(r)
    h = np.cross(r, v)
    y_orb = h / np.linalg.norm(h)
    x_orb = np.cross(y_orb, z_orb)
    return np.vstack([x_orb, y_orb, z_orb]).T

def get_rotation_matrix(file='logs/beacon_human.csv'):
    mas = []
    with open(file, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            if row and row[0] != 'time usec':
                try:
                    mas.append([float(i) for i in row])
                except ValueError:
                    continue

    c = []
    for i in mas:
        quat = [i[1], i[2], i[3], i[4]]
        rot_matrix = quaternion_to_rotation_matrix(quat)
        c.append(rotation_matrix_to_euler(rot_matrix))

    latitude = np.radians(mas[0][9])
    longitude = np.radians(mas[0][10])
    altitude = mas[0][11]

    r = np.array([
        (6378.1 + altitude) * np.cos(latitude) * np.cos(longitude),
        (6378.1 + altitude) * np.cos(latitude) * np.sin(longitude),
        (6378.1 + altitude) * np.sin(latitude)
    ])

    v_direction = np.cross([0, 0, 1], r)
    v_direction /= np.linalg.norm(v_direction)
    orbital_speed = math.sqrt(398600 / np.linalg.norm(r))
    v = v_direction * orbital_speed

    cc = []
    for i in c:
        R_eci = euler_to_rotation_matrix(i[0], i[1], i[2])
        T_eci_to_orb = eci_to_orb_matrix(r, v)
        R_orb = T_eci_to_orb @ R_eci
        cc.append(R_orb)

    orb_matrix = []
    for i in cc:
        orb_matrix.append(rotation_matrix_to_euler(i))

    return orb_matrix
