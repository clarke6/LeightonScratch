from sklearn import svm
from datetime import datetime
from numpy import zeros

filename = raw_input('Enter name of file to read: ')
data = open(filename,'r').read()
dataArray = data.split('\n')
Date = dataArray[-2].split(',')[2]
endDay = Date[8:10]
Date = dataArray[0].split(',')[2]
startDay = Date[8:10]
YearMonth = Date[:8]
numDays = int(endDay) - int(startDay) + 1
plotData = zeros((numDays,4))

for eachLine in dataArray:
    if len(eachLine) > 1:
        dataLine = eachLine.split(',')
        if dataLine[4] == '3' and dataLine[6] == '1':
            day = int(dataLine[2][8:10]) - int(startDay)
            date_dt = datetime.strptime(YearMonth+dataLine[2][8:10], '%Y-%m-%d')
            if datetime.strftime(date_dt, '%A') == 'Saturday' or datetime.strftime(date_dt, '%A') == 'Sunday':
                plotData[day][3] = 1
            hour = int(dataLine[2][11:13])
            if hour > 5:
                if hour < 11:
                    group = 0
                elif hour >= 11 and hour < 17:
                    group = 1
                elif hour >=17:
                    group = 2
                plotData[day][group] += 1
