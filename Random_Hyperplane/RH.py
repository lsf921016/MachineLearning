import sys
import array
import random
from sklearn.svm import LinearSVC
from os import chdir


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


def dot_product(a1, a2):
    a = 0
    for i in range(0, len(a1), 1):
        a += a1[i] * a2[i];
    return a


def sign(num):
    return -1 if num < 0 else 1


def norm(vector):
    return sum(i * i for i in vector)


def create_w(ncols):
    w = array.array("f", [])
    for i in range(ncols):
        w.append(random.uniform(-1, 1))
    return w


def projection(datapoint, w):
    dp = dot_product(datapoint, w)
    normw = norm(w)
    proj = [i * dp / normw for i in w]
    return proj


def getZi(data, w):
    Zi = []
    for datapoint in data:
        value = dot_product(datapoint, w)
        sign_value = sign(value)
        z = (1 + sign_value) / 2
        Zi.append(z)
    return Zi


def getZ(data, k):
    Z = []
    ncols = len(data[0])
    for i in range(k):
        w = create_w(ncols)
        Z.append(getZi(data, w))
    return list(map(list, zip(*Z)))


def get_score(prediction, labels):
    count = 0
    n = len(prediction)
    for i in range(0, n):
        if prediction[i] == labels[i]:
            count += 1
    return count / n


def kford_validation(clf, data, labels, k):
    rows = len(data)
    cols = len(data[0])
    batch = int(rows / k)
    scores = []
    for i in range(0, k):
        start = i * batch
        end = (i + 1) * batch
        test_x_set = data[start:end]
        train_x_set = data[0:start] + data[end:rows]
        test_y_set = labels[start:end]
        train_y_set = labels[0:start] + labels[end:rows]
        clf.fit(train_x_set, train_y_set)
        prediction = clf.predict(test_x_set)
        scores.append(get_score(prediction, test_y_set))
    return scores


def seperatedata(data, labels):
    train=[]
    for i in range(0,len(labels)):
        if labels[i]!=None:
            train.append(data[i])
    test=[]
    for i in range(0,len(data)):
        if data[i] not in train:
            test.append(data[i])
    return train, test


def get_erro_on_6datasets(data_folder):
    chdir(data_folder)
    datafiles = ["breast_cancer.data",
                 "climate.data",
                 "hill_valley.data",
                 "ionosphere.data",
                 "micromass.data",
                 "qsar.data"]
    labelfiles = ["breast_cancer.labels",
                  "climate.labels",
                  "hill_valley.labels",
                  "ionosphere.labels",
                  "micromass.labels",
                  "qsar.labels"]
    origin_errors = {}
    new_errors={}
    for dataset_name,label_name in zip(datafiles, labelfiles):
        print(dataset_name)
        data=loadData(dataset_name)
        print(len(data))

        print(label_name)
        labels=loadLabel(label_name)
        print(len(labels))
        origin_errors[dataset_name]=[]
        new_errors[dataset_name]=[]
        for k in (10,100,1000,10000):
            Z=getZ(data,k)
            clf=LinearSVC()
            #origin
            score=kford_validation(clf,data,labels,10)
            origin_errors[dataset_name].append(score)
            #new representation
            score=kford_validation(clf,Z,labels,10)
            new_errors[dataset_name].append(score)
    print(origin_errors)
    print(new_errors)

if __name__ == '__main__':
    datafile = sys.argv[1]
    labelfile = sys.argv[2]

    data = loadData(datafile)
    labels = loadLabel(labelfile)

    rows = len(data)
    cols = len(data[0])

    train ,test =seperatedata(data,labels)
    print(data)
    print(train)
    print(test)
    k=2
    Z = getZ(train, k)
    clf = LinearSVC()
    #origin
    clf.fit(train, labels)
    predictions = clf.predict(test)
    print("on origin dataset")
    print(predictions)

    #new representation
    clf.fit(Z,labels)
    predictions=clf.predict(test)
    print("on new data set: ")
    print(predictions)
    get_erro_on_6datasets("D:\datasets")
