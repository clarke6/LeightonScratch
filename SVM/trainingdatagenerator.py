from numpy.random import normal, uniform

cat1 = []
while len(cat1)<100:
    new = []
    morn = uniform(0,1)
    new.append(morn)
    aft = uniform(0,0.1)
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
    aft = uniform(0,0.1)
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
    aft = uniform(0.1,1)
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
    aft = uniform(0.1,1)
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
    aft = uniform(0,0.1)
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
    aft = uniform(0,0.1)
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
    aft = uniform(0.1,1)
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
    aft = uniform(0.1,1)
    new.append(aft)
    eve = uniform(0,1)
    while eve <= morn:
        eve = uniform(0,1)
    new.append(eve)
    train4.append(new)
