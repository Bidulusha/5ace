import csv
from decimal import Decimal
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd

mas = []

with open('logs/beacon_human.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        if row != [] and row[0] != 'time usec':
            l = []
            for i in row:
                n = Decimal(i)
                l.append(n)
            mas.append(l)


'''mm = []
for i in mas:
    quaternion = (i[1],i[2],i[3],i[4])  
    rot = Rotation.from_quat(quaternion)
    rot_euler = rot.as_euler('xyz', degrees=True)
    rr = list(rot_euler)
    mm.append(rr)'''

x = []
y = []
z = []


fig = plt.figure()
ax = fig.add_subplot(projection='3d')
plt.plot([0, mm[0][0]], [0, mm[0][1]], [0, mm[0][2]], color = 'red')
plt.plot([0,float(mas[0][6]) * 100 ], [0,float(mas[0][7])* 100], [0,float(mas[0][8])* 100]) # 6 7 8
plt.show()


'''timemas = [31557600000000, 86400000000, 3600000000, 60000000, 1000000]
datemas = []

for i in mas:
    t = int(i[0])
    date = []
    for j in timemas:
        date.append(t // j)
        t %= j
    datemas.append(date)

print(datemas)'''

'''x = [] #9
y = [] #10 

for i in mas:
    x.append(i[0])
    y.append(i[1])

plt.plot(x, y)
plt.show()'''
