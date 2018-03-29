import sys
import math
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
        scores.append(get_score(prediction,test_y_set))
    return scores


def dot_product(a1, a2):
    a = 0
    for i in range(0, len(a1), 1):
        a += a1[i] * a2[i];
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
testfile = sys.argv[3]
output_file = sys.argv[4]

data = loadData(datafile)
labels = loadLabel(labelfile)
test_data = loadData(testfile)

rows = len(data)
cols = len(data[0])

coe = [0] * cols

# compute coefficient
n = len(labels)
mean_y = sum(labels[i] for i in range(n)) / n
theta_y = math.sqrt(sum((labels[i] - mean_y) ** 2 for i in range(n)))
for j in range(0, cols):
    mean_x = sum(data[i][j] for i in range(rows))/rows
    cov = sum((data[i][j] - mean_x) * (labels[i] - mean_y) for i in range(rows))
    theta_x = math.sqrt(sum((data[i][j] - mean_x) ** 2 for i in range(rows)))
    if theta_x==0:
        coe[j]=0
    else:
        coe[j] = cov / (theta_x * theta_y)
# print(coe)

sample_list = []
for i in range(0, 15):
    max_coe = max(coe)
    print(max_coe)
    for j in range(0, len(coe)):
        if coe[j] == max_coe:
            sample_list.append(j)
            coe[j]=-99999
print("15 features has been selected")
print("the select features index list is:")
print(sample_list)

# sample the data
s_data = []
for i in range(rows):
    record = []
    for j in range(cols):
        if j in sample_list:
            record.append(data[i][j])
    s_data.append(record)

#sample test data
s_test_data=[]
t_rows=len(test_data)
t_cols=len(test_data[0])
for i in range(t_rows):
    record=[]
    for j in range(t_cols):
        if j in sample_list:
            record.append(test_data[i][j])
    s_test_data.append(record)

# define the method

clf=svm.SVC(kernel='linear', C=1)

# 10-ford validation
#x_train, x_test, y_train, y_test = train_test_split(s_data, labels, test_size=0.1, random_state=0)
#clf = svm.SVC(kernel='linear', C=1).fit(x_train, y_train)
#print("use function to get score:")
#sss=clf.score(x_test, y_test)
#print(sss)
#clf.predict(s_test_data)

scores=kford_validation(clf,s_data,labels,10)


# train the model
clf.fit(s_data,labels)

# predict the test data
prediction=clf.predict(s_test_data)


#output the prediction into file and cmd
f=open(output_file,'w')
n=len(prediction)

for i in range(0,n):
    print("%d %d"%(prediction[i],i))

for i in range(0,n):
    f.write(str(prediction[i]))
    f.write(" ")
    f.write(str(i))
    f.write("\n")
f.close()

