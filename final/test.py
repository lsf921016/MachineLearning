import sys
import math
from sklearn.model_selection import train_test_split, cross_val_predict
from sklearn.model_selection import cross_val_score
from sklearn import svm


def get_score(prediction, labels):
    count=0
    n=len(prediction)
    for i in range(0,n):
        if prediction[i]==labels[i]:
            count+=1
    return count/n


def kford_validation(clf,data,labels,k):
    rows=len(data)
    cols=len(data[0])
    batch=int(rows/k)
    scores=[]
    for i in range(0,k):
        start=i*batch
        end=(i+1)*batch
        test_x_set=data[start:end]
        train_x_set=data[0:start]+data[end:rows]
        test_y_set=labels[start:end]
        train_y_set=labels[0:start]+labels[end:rows]
        clf.fit(train_x_set,train_y_set)
        prediction=clf.predict(test_x_set)
        print("batch %d"%(i))
        print("test set is from %d to %d"%(start,end))
        print("train set is 0--%d %d--%d"%(start,end,rows))
        print("length of train set %d"%(len(train_x_set)))
        scores.append(get_score(prediction,test_y_set))
    return scores
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
    labels = []

    i = 0;
    l = f.readline()
    while l != '':
        a = l.split()
        labels.append(int(a[0]))
        l = f.readline()
    return labels

def mean(a):
    tot=0
    n=len(a)
    for i in range(0,n):
        tot+=a[i]
    return tot/n


datafile = sys.argv[1]
labelfile = sys.argv[2]

data = loadData(datafile)
labels = loadLabel(labelfile)

clf=svm.SVC(kernel='linear', C=1)
# 10-ford validation
x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.05, random_state=0)
clf = svm.SVC(kernel='linear', C=1).fit(x_train, y_train)
ss=clf.score(x_test, y_test)
print(ss)

scores=kford_validation(clf,data,labels,20)
print(scores)
print(mean(scores))



# predict the test data
prediction=clf.predict(s_test_data)


#output the prediction into file and cmd
f=open(output_file,'w')
n=len(prediction)

for i in range(0,n):
    print("%d %d"%(prediction[i],i))
