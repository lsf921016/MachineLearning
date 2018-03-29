import sys
import random
import math

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
        data.append(l2)
        l = f.readline()
    return data


def v_plus(a, b):
    cols = len(a)
    c = [0] * cols
    for i in range(0, cols):
        c[i] = a[i] + b[i]
    return c

def v_divide(a,n):
    cols=len(a)
    for i in range(0,cols):
        a[i]=a[i]/n
    return a
def cal_means(data, c):
    n0 = 0
    n1 = 0
    rows = len(data)
    cols = len(data[0])
    m0 = [0] * cols
    m1 = [0] * cols
    for i in range(0, rows):
        if c[i] == 0:
            m0 = v_plus(m0, data[i])
            n0 += 1
        else:
            m1 = v_plus(m1, data[i])
            n1 += 1

    m0 = [0]*cols if n0 == 0 else v_divide(m0, n0)
    m1 = [0]*cols if n1 == 0 else v_divide(m1, n1)
    return m0, m1
def dist(a, b):
    cols = len(a)
    d = 0
    for i in range(0, cols):
        d += (a[i] - b[i]) ** 2
    return math.sqrt(d)

datafile = sys.argv[1]
data = loadData(datafile)
rows = len(data)
cols = len(data[0])
print(data)
# initialize
c = [0] * rows
for i in range(0, rows):
    c[i] = random.randint(0, 1)
m0, m1 = cal_means(data, c)

convergence=.0001
difference=1
error=0
#update
while difference>convergence:
    for i in range(0,rows):
        if dist(data[i],m0)<dist(data[i],m1):
            c[i]=0
        else:
            c[i]=1
    m0,m1=cal_means(data,c)

    # compute difference
    new_error=0
    for i in range(0,rows):
        if c[i]==0:
            new_error+=dist(m0,data[i])**2
        if c[i]==1:
            new_error+=dist(m1,data[i])**2
    difference=abs(new_error-error)
    error=new_error

    print("difference:   %f"%(difference))
    print("error :  %f"%(error))

print(c)

