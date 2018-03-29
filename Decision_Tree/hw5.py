import sys

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

datafile = sys.argv[1]
labelfile = sys.argv[2]

data = loadData(datafile)
labels = loadLabel(labelfile)

rows = len(data)
cols = len(data[0])

splits=[0]*cols
ginis=[0]*cols
for i in range(0,cols):
    thresholds=[]
    values=[]
    for j in range(0,rows):
        value=data[j][i]
        if value not in values:
            values.append(value)
    values.sort()
    for k in range(0,len(values)-1):
        thresholds.append((values[k]+values[k+1])/2)

    gini=sys.maxsize
    split=0
    for k in range(0,len(thresholds)):
        lsize=0
        rsize=0
        lp=0
        rp=0
        for j in range(0,rows):
            if data[j][i]<thresholds[k]:
                lsize+=1
                if labels[j]==0:
                    lp+=1
            else:
                rsize+=1
                if labels[j]==0:
                    rp+=1

        new_gini=(lsize/rows)*(lp/lsize)*(1 - lp/lsize) + (rsize/rows)*(rp/rsize)*(1 - rp/rsize)
        if(new_gini<gini):
            gini=new_gini
            split=thresholds[k]
    splits[i]=split
    ginis[i]=gini

print(ginis)

min_gini=min(ginis)
for i in range(0,len(splits)):
    if ginis[i]==min_gini:
        print("Best_column : %d"%i)
        print("Gini is %f: "%ginis[i])
        print("Split point's value : %f"%splits[i])
        break

output_file = sys.argv[3]
f = open(output_file, 'w')
for i in range(0,len(splits)):
    f.write(str(i+1))
    f.write("\t")
    f.write(str(splits[i]))
    f.write("\r")
f.close()

