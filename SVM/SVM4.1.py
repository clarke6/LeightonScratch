from numpy.random import normal, uniform
from sklearn import svm

results = [0,0,0,0]
for i in range(100):
    cat1 = []
    while len(cat1)<100:
        new = []
        morn = uniform(0,1)
        new.append(morn)
        aft = uniform(0,0.5)
        new.append(aft)
        eve = uniform(0,1)
        while eve >= morn:
            eve = uniform(0,1)
        new.append(eve)
        cat1.append(new)

    cat2 = []
    while len(cat2)<100:
        new = []
        morn = uniform(0,1)
        new.append(morn)
        aft = uniform(0,0.5)
        new.append(aft)
        eve = uniform(0,1)
        while eve <= morn:
            eve = uniform(0,1)
        new.append(eve)
        cat2.append(new)

    cat3 = []
    while len(cat3)<100:
        new = []
        morn = uniform(0,1)
        new.append(morn)
        aft = uniform(0.5,1)
        new.append(aft)
        eve = uniform(0,1)
        while eve >= morn:
            eve = uniform(0,1)
        new.append(eve)
        cat3.append(new)

    cat4 = []
    while len(cat4)<100:
        new = []
        morn = uniform(0,1)
        new.append(morn)
        aft = uniform(0.5,1)
        new.append(aft)
        eve = uniform(0,1)
        while eve <= morn:
            eve = uniform(0,1)
        new.append(eve)
        cat4.append(new)

    train1 = []
    while len(train1)<100:
        new = []
        morn = uniform(0,1)
        new.append(morn)
        aft = uniform(0,0.5)
        new.append(aft)
        eve = uniform(0,1)
        while eve >= morn:
            eve = uniform(0,1)
        new.append(eve)
        train1.append(new)

    train2 = []
    while len(train2)<100:
        new = []
        morn = uniform(0,1)
        new.append(morn)
        aft = uniform(0,0.5)
        new.append(aft)
        eve = uniform(0,1)
        while eve <= morn:
            eve = uniform(0,1)
        new.append(eve)
        train2.append(new)

    train3 = []
    while len(train3)<100:
        new = []
        morn = uniform(0,1)
        new.append(morn)
        aft = uniform(0.5,1)
        new.append(aft)
        eve = uniform(0,1)
        while eve >= morn:
            eve = uniform(0,1)
        new.append(eve)
        train3.append(new)

    train4 = []
    while len(train4)<100:
        new = []
        morn = uniform(0,1)
        new.append(morn)
        aft = uniform(0.5,1)
        new.append(aft)
        eve = uniform(0,1)
        while eve <= morn:
            eve = uniform(0,1)
        new.append(eve)
        train4.append(new)

    bins = [1]*100+[2]*100+[3]*100+[4]*100
    training = train1+train2+train3+train4

    clf = svm.SVC()
    clf.fit(training,bins)

    correct = 0
    for eachEntry in clf.predict(cat1):
        if eachEntry == 1:
            correct +=1
    acc1 = float(correct) / len(cat1) * 100
    results[0] += acc1

    correct = 0
    for eachEntry in clf.predict(cat2):
        if eachEntry == 2:
            correct +=1
    acc2 = float(correct) / len(cat2) * 100
    results[1] += acc2

    correct = 0
    for eachEntry in clf.predict(cat3):
        if eachEntry == 3:
            correct +=1
    acc3 = float(correct) / len(cat3) * 100
    results[2] += acc3

    correct = 0
    for eachEntry in clf.predict(cat4):
        if eachEntry == 4:
            correct +=1
    acc4 = float(correct) / len(cat4) * 100
    results[3] += acc4

for k in range(len(results)):
    results[k] = results[k] / 100

print '\nAccuracy by category:\n'
print 'Category 1: %g%% \n' % (results[0])
print 'Category 2: %g%% \n' % (results[1])
print 'Category 3: %g%% \n' % (results[2])
print 'Category 4: %g%% \n' % (results[3])
