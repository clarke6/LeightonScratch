from numpy import zeros, argmax, unravel_index
import matplotlib.pyplot as plt
from datetime import datetime

filename = raw_input('Enter name of file to read: ')
data = open(filename,'r').read()
dataArray = data.split('\n')
Date = dataArray[-2].split(',')[2]
endDay = Date[8:10]
Date = dataArray[0].split(',')[2]
startDay = Date[8:10]
YearMonth = Date[:8]
numDays = int(endDay) - int(startDay) + 1
plotData = zeros((numDays,24))

for eachLine in dataArray:
    if len(eachLine) > 1:
        dataLine = eachLine.split(',')
        if dataLine[4] == '3' and dataLine[6] == '1':
            day = int(dataLine[2][8:10]) - int(startDay)
            hour = int(dataLine[2][11:13])
            plotData[day][hour] += 1

fig1 = plt.figure()
x1 = range(24)
x2 = range(1,numDays + 1)
daynames=[]
totalUsage = zeros(numDays)
maxIndex = unravel_index(plotData.argmax(), plotData.shape)
maxEntry = plotData[maxIndex]
for k in range(len(plotData)):
    fig1.add_subplot(2,4,k+1)
    plt.bar(x1,plotData[k])
    plt.axis([0,23,0,maxEntry])
    plt.xticks(range(24)[0::2])
    plt.ylabel('Minutes of Use')
    plt.xlabel('Hour of Day')
    day = int(startDay) + k
    Date = YearMonth + str(day)
    fmtDate = datetime.strptime(Date, '%Y-%m-%d')
    daynames.append(datetime.strftime(fmtDate, '%A'))
    plt.title(daynames[k] + ', ' + datetime.strftime(fmtDate,'%m-%d-%Y'))
    totalUsage[k] = sum(plotData[k])
fig1.add_subplot(2,4,8)
plt.bar(x2,totalUsage)
plt.xticks(x2, daynames)
plt.xticks(rotation=45)
plt.title('Total Usage by Day')
plt.ylabel('Minutes of Use')
plt.xlabel('Day of Week')


