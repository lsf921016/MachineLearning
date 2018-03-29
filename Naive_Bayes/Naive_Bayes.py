# read data from file
import sys
import math

datafile = sys.argv[1]
f = open(datafile, 'r')

data = []
i = 0;
l = f.readline()
while l != '':
    a = l.split()
    l2 = []
    for j in range(0, len(a), 1):
        l2.append(float(a[j]))
    data.append(l2)
    l = f.readline()

rows = len(data)
cols = len(data[0])

# read labels from file

trainlabelfile = sys.argv[2]
f = open(trainlabelfile, 'r')
trainlabels = {}

i = 0;
l = f.readline()
while l != '':
    a = l.split()
    trainlabels[int(a[1])] = int(a[0])
    l = f.readline()

# calculate mean
m0 = []
m1 = []
for i in range(0, cols, 1):
    m0.append(0)
    m1.append(0)
n0 = 0
n1 = 0
for i in range(0, rows, 1):
    if (trainlabels.get(i) != None and trainlabels[i] == 0):
        n0 += 1
        for j in range(0, cols, 1):
            m0[j] += data[i][j]
    if (trainlabels.get(i) != None and trainlabels[i] == 1):
        n1 += 1
        for j in range(0, cols, 1):
            m1[j] += data[i][j]

for j in range(0, cols, 1):
    m0[j] /= n0
    m1[j] /= n1

# calculate stardard deviation

s0 = []
s1 = []
s = []
for i in range(cols):
    s0.append(0)
    s1.append(0)
    s.append(0)

for i in range(rows):
    if (trainlabels.get(i) != None and trainlabels[i] == 0):
        for j in range(0, cols, 1):
            s0[j] += (data[i][j] - m0[j]) ** 2
    if (trainlabels.get(i) != None and trainlabels[i] == 1):
        for j in range(0, cols, 1):
            s1[j] += (data[i][j] - m1[j]) ** 2

sum0 = 0
sum1 = 0

for i in range(cols):
    s0[i] = s0[i] / n0
    sum0 = sum0 + math.log(math.sqrt(s0[i]))
    s1[i] = s1[i] / n1
    sum1 = sum1 + math.log(math.sqrt(s1[i]))

##classify unlabeled points

for i in range(0, rows, 1):
    if trainlabels.get(i) == None:
        d0 = 0
        d1 = 0
        for j in range(0, cols, 1):
            d0 = d0 + ((data[i][j] - m0[j]) ** 2 / s0[j]) + sum0
            d1 = d1 + ((data[i][j] - m1[j]) ** 2 / s1[j]) + sum1
            d0 = d0 + ((data[i][j] - m0[j]) ** 2 / s0[j])
            d1 = d1 + ((data[i][j] - m1[j]) ** 2 / s1[j])

        print("d0=", d0, "d1=", d1)
        if d0 < d1:
            print ("0", i)
        else:
            print ("1", i)
