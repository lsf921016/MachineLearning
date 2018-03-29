import sys
import random
import math

def dot_product(a1, a2):
    a=0
    for i in range(0,len(a1),1):
        a+=a1[i]*a2[i];
    return a


def loadData(datafile):
    f = open(datafile, 'r')
    data = []
    i = 0;
    l = f.readline()
    while l != '':
        a = l.split()
        l2 = []
        for j in range(0, len(a), 1):
            l2.append(float(a[j]))
        l2.append(1)
        data.append(l2)
        l = f.readline()
    return data


def loadLabel(labelfile):
    f = open(labelfile, 'r')
    labels = {}

    i = 0;
    l = f.readline()
    while l != '':
        a = l.split()
        labels[int(a[1])] = int(a[0])
        l = f.readline()
    return labels


datafile = sys.argv[1]
labelfile = sys.argv[2]

data = loadData(datafile)
labels = loadLabel(labelfile)

rows = len(data)
cols = len(data[0])

# initialize w
w = [0]*cols
for i in range(0, cols, 1):
    w[i] = .02 * random.random() - .01

# gradient descent

eta = .01
convergence = 0.000000001
new_error=1
error=1
while (abs(new_error) > convergence):
    # compute delf
    delf = [0] * cols
    for i in range(0, rows, 1):
        if (labels[i] != None):
            dp = dot_product(w, data[i])
            factor=labels[i]-1/(1+math.e**(-dp))
            for j in range(0,cols,1):
                delf[j] = delf[j] +data[i][j]*factor

    # update
    for j in range(0, cols, 1):
        w[j] = w[j] + eta * delf[j]

    ##compute error
    prev=error
    error = 0
    for i in range(0, rows, 1):
        if (labels[i] != None):
            dp = dot_product(w, data[i])
            error = error + (labels[i] - 1/(1+math.e**(-dp))) ** 2

    new_error = prev - error
    print("error=",new_error)
##gradient over

##output results
print("w=", w)
normw = 0
for j in range(0, cols - 1, 1):
    normw = normw + w[j] ** 2
normw = math.sqrt(normw)
print("||w||=", normw)

d_origin = w[len(w) - 1] / normw
print("distance to origin=", d_origin)

##prediction
output_file = sys.argv[3]
f = open(output_file, 'w')
for i in range(0, rows, 1):
    if (labels[i] == None):
        dp = dot_product(w, data[i])
        if dp > 0:
            print("1 " + i)
        else:
            print("-1 " + i)
f.close()

## python svm.py input labels output
