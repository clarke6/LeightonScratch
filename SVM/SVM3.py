from numpy import zeros, argmax, unravel_index
from datetime import datetime
from sklearn import svm

training = [[1,0,0.5,0],[1,0.5,0.5,0],[0.5,0,1,0],[0.5,0.5,1,0]]
bins = [1,2,3,4]
clf = svm.SVC()
clf.fit(training,bins)

sumVars = []
winVars = []
sumPredictions = []
winPredictions = []
for i in range(1,6):
    sumFile = 'summer' + str(i) + '.csv'
    winFile = 'winter' + str(i) + '.csv'
    sumData = open(sumFile, 'r').read()
    sumDataArray = sumData.split('\n')
    sumEndDate = sumDataArray[-2].split(',')[2][0:10]
    sumEndDate = datetime.strptime(sumEndDate, '%Y-%m-%d')
    sumStartDate = sumDataArray[0].split(',')[2][0:10]
    sumStartDate = datetime.strptime(sumStartDate, '%Y-%m-%d')
    sumNumDays = (sumEndDate - sumStartDate).days + 1
    sumInputs = zeros((sumNumDays, 4))
    winData = open(winFile, 'r').read()
    winDataArray = winData.split('\n')
    winEndDate = winDataArray[-2].split(',')[2][0:10]
    winEndDate = datetime.strptime(winEndDate, '%Y-%m-%d')
    winStartDate = winDataArray[0].split(',')[2][0:10]
    winStartDate = datetime.strptime(winStartDate, '%Y-%m-%d')
    winNumDays = (winEndDate - winStartDate).days + 1
    winInputs = zeros((winNumDays, 4))

    for eachLine in sumDataArray:
        if len(eachLine) > 1:
            dataLine = eachLine.split(',')
            if dataLine[4] == '3' and dataLine[6] == '1':
                date = datetime.strptime(dataLine[2][0:10], '%Y-%m-%d')
                day = (date-sumStartDate).days
                if datetime.weekday(date) == 5 or datetime.weekday(date) == 6:
                    sumInputs[day][3] = 1
                hour = int(dataLine[2][11:13])
                if hour > 5:
                    if hour < 12:
                        group = 0
                    elif hour < 18:
                        group = 1
                    elif hour <= 23:
                        group = 2
                    sumInputs[day][group] += 1

    for eachLine in sumInputs:
        maxIndex = eachLine.argmax()
        maxEntry = eachLine[maxIndex]
        for j in range(3):
            eachLine[j] = eachLine[j] / maxEntry

    sumVars.append(sumInputs)

    for eachLine in winDataArray:
        if len(eachLine) > 1:
            dataLine = eachLine.split(',')
            if dataLine[4] == '3' and dataLine[6] == '1':
                date = datetime.strptime(dataLine[2][0:10], '%Y-%m-%d')
                day = (date-winStartDate).days
                if datetime.weekday(date) == 5 or datetime.weekday(date) == 6:
                    winInputs[day][3] = 1
                hour = int(dataLine[2][11:13])
                if hour > 5:
                    if hour < 12:
                        group = 0
                    elif hour < 18:
                        group = 1
                    elif hour <= 23:
                        group = 2
                    winInputs[day][group] += 1

    for eachLine in winInputs:
        maxIndex = eachLine.argmax()
        maxEntry = eachLine[maxIndex]
        for j in range(3):
            eachLine[j] = eachLine[j] / maxEntry

    winVars.append(winInputs)
    
for i in range(len(sumVars)):
    sumPredictions.append(clf.predict(sumVars[i]))
print '\n Summer Predictions \n'
print sumPredictions

for i in range(len(winVars)):
    winPredictions.append(clf.predict(winVars[i]))
print '\n Winter Predictions \n'
print winPredictions
    
