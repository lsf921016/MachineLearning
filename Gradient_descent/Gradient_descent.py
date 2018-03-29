import sys
import random
import math
import numpy as np

# read data and labels from file


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
    l2.append(1)
    data.append(l2)
    l = f.readline()

rows = len(data)
cols = len(data[0])
ref = data[0]
# read labels from file

trainlabelfile = sys.argv[2]
f = open(trainlabelfile, 'r')
classes = {}
class_size=[0,0]
i = 0;
l = f.readline()
while l != '':
    a = l.split()
    classes[int(a[1])] = int(a[0])
    class_size[int(a[0])]=class_size[int(a[0])]+1
    if(classes[int(a[1])]==0):
        classes[int(a[1])]=-1
    l = f.readline()

# initialize w

w = []
for i in range(0,cols,1):
    w.append(0)

for i in range(0, cols, 1):
    w[j] = .02 * random.random() - .01

##gradient descent iteration

eta = .0001

for k in range(0, 10000, 1):
    #compute dellf
    dellf = []
    for i in range(0,cols,1):
        dellf.append(0)
    for i in range(0, rows, 1):
        if (classes[i] != None):
            dp = np.dot(w, data[i])
            for j in range(0, cols, 1):
                dellf[j] = dellf[j] + (classes[i] - dp) * data[i][j]

    ##update
    for j in range(0, cols, 1):
        w[j] = w[j] + eta * dellf[j]

    error = 0

    ##compute error
    for i in range(0, rows, 1):
        if (classes[i] != None):
            error = error + (classes[i] - np.dot(w, data[i])) ** 2
    print ("error=",error)

print ("w=")
normw=0;
for j in range(0,cols-1,1):
    normw=normw+w[j]**2
    print (w[j])
print ("\n")
normw=math.sqrt(normw)
print ("||w||=",normw)
d_origin=w[len(w)-1]/normw;
print ("distance to origin=",d_origin)

##prediction
output_file=sys.argv[3]
f=open(output_file,'w')
for i in range(0,rows,1):
    if(classes[i]==None):
        dp=np.dot(w,data[i])
        if dp>0:
            print ("1 "+i)
        else:
            print ("0 "+i)
f.close()


