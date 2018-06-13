from numpy import zeros, argmax, unravel_index
from datetime import datetime
from sklearn import svm

training = [[1,0,0.5,0],[1,0.5,0.5,0],[0.5,0,1,0],[0.5,0.5,1,0]]
bins = [1,2,3,4]
clf = svm.SVC()
clf.fit(training,bins)

allData = []
predictions = []
for i in range(1,6):
    filename = 'summer' + str(i) + '.csv'
    data = open(filename, 'r').read()
    dataArray = data.split('\n')
    endDate = dataArray[-2].split(',')[2][0:10]
    endDate = datetime.strptime(endDate, '%Y-%m-%d')
    startDate = dataArray[0].split(',')[2][0:10]
    startDate = datetime.strptime(startDate, '%Y-%m-%d')
    numDays = (endDate - startDate).days + 1
    inputs = zeros((numDays, 4))

    for eachLine in dataArray:
        if len(eachLine) > 1:
            dataLine = eachLine.split(',')
            if dataLine[4] == '3' and dataLine[6] == '1':
                date = datetime.strptime(dataLine[2][0:10], '%Y-%m-%d')
                day = (date-startDate).days
                if datetime.weekday(date) == 5 or datetime.weekday(date) == 6:
                    inputs[day][3] = 1
                hour = int(dataLine[2][11:13])
                if hour > 5:
                    if hour < 12:
                        group = 0
                    elif hour < 18:
                        group = 1
                    elif hour <= 23:
                        group = 2
                    inputs[day][group] += 1

    for eachLine in inputs:
        maxIndex = eachLine.argmax()
        maxEntry = eachLine[maxIndex]
        for j in range(3):
            eachLine[j] = eachLine[j] / maxEntry

    allData.append(inputs)
    
for i in range(len(allData)):
    predictions.append(clf.predict(allData[i]))
print predictions
    
