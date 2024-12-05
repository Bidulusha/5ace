import csv
from decimal import Decimal
import matplotlib.pyplot as plt

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


raz = []

for i in range(1, len(mas)):
    raz.append((i, mas[i][0] - mas[i - 1][0]))

for i in raz:
    print(*i)
'''x = [] #9
y = [] #10 

for i in mas:
    x.append(i[0])
    y.append(i[1])

plt.plot(x, y)
plt.show()'''
