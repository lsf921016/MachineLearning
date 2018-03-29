import sys

import random


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

def get_sample(data):
    rows=len(data)
    cols=len(data[0])
    f_cols=int(cols/3)
    if f_cols<1:
        f_cols=1
    sample=[]
    for i in range(0,rows):
        sample.append([0]*f_cols)
    for j in range(0,f_cols):
        temp = []
        sel = random.randint(0, cols - 1)
        while sel in temp:
            sel = random.randint(0, cols - 1)
        temp.append(sel)
        for i in range(0,rows):
            sample[i][j]=data[i][sel]
    return sample

def get_splits(data,labels):
    rows = len(data)
    cols = len(data[0])

    splits = [0] * cols
    ginis=[0]*cols
    for i in range(0, cols):
        thresholds = []
        values = []
        for j in range(0, rows):
            value = data[j][i]
            if value not in values:
                values.append(value)

        values.sort()
        for k in range(0, len(values) - 1):
            thresholds.append((values[k] + values[k + 1]) / 2)

        gini = sys.maxsize
        split = 0
        for k in range(0, len(thresholds)):
            lsize = 0
            rsize = 0
            lp = 0
            rp = 0
            for j in range(0, rows):
                if data[j][i] < thresholds[k]:
                    lsize += 1
                    if labels[j] == -1:
                        lp += 1
                else:
                    rsize += 1
                    if labels[j] == -1:
                        rp += 1

            new_gini = (lsize / rows) * (lp / lsize) * (1 - lp / lsize) + (rsize / rows) * (rp / rsize) * (
            1 - rp / rsize)
            if (new_gini < gini):
                gini = new_gini
                split = thresholds[k]
        ginis[i]=gini
        splits[i] = split
    return splits,ginis

def get_mode(arr):
    length=len(arr)
    if length==0:
        return None
    if length<=2:
        return arr[0]
    count={}
    for item in arr:
        if item in count:
            count[item]+=1
        else:
            count[item]=1
    mode=0
    max=0
    for key in count.keys():
        if count[key]>max:
            mode=key
            max=count[key]
    return mode

datafile = sys.argv[1]
labelfile = sys.argv[2]

data = loadData(datafile)
labels = loadLabel(labelfile)

rows = len(data)
cols = len(data[0])

votes=[]
for i in range(0,rows):
    votes.append([0]*100)

for i in range(0,100):
    sample=get_sample(data)
    rows=len(sample)
    splits,ginis=get_splits(sample,labels)
    min_ginus=min(ginis)
    sel_col=0
    for k in range(0,len(ginis)):
        if ginis[k]==min_ginus:
            sel_col=k
    for j in range(0,rows):
        if sample[j][sel_col]<splits[sel_col]:
            votes[j][i]=-1
        else:
            votes[j][i]=1

res=[0]*rows
for i in range(0,rows):
    res[i]=get_mode(votes[i])

for i in range(0,len(res)):
    print("%d  %d"%(res[i],i))



