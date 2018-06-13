from numpy import zeros, argmax, unravel_index
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

filename = raw_input('Enter the name of file to read: ')
startDay = raw_input('Enter first day of desired week (M/D): ')
startDay_dt = datetime.strptime(startDay, '%m/%d')
startDay_dt = startDay_dt.replace(year=datetime.now().year)
endDay_dt = startDay_dt + timedelta(days = 6)
dateList = []
for i in range(7):
    dateList.append(startDay_dt + timedelta(days = i))
data = open(filename,'r').read()
dataArray = data.split('\n')
volData = zeros((7,24))
enData = zeros((7,24))

for eachLine in dataArray:
    if len(eachLine) > 1 and eachLine[0].isdigit():
        dataLine = eachLine.split(',')
        lineDate = dataLine[0].split(' ')
        lineDate_dt = datetime.strptime(lineDate[0], '%m/%d').replace(year=datetime.now().year)
        if lineDate_dt >= startDay_dt and lineDate_dt <= endDay_dt:
            lineTime_dt = datetime.strptime(lineDate[1]+lineDate[2], '%I:%M:%S%p')
            row = dateList.index(lineDate_dt)
            col = lineTime_dt.hour
            volData[row][col] += float(dataLine[1])*float(dataLine[4])/60

data = open('Book2.csv','r').read()
dataArray = data.split('\r\n')
mainsArray = []

for eachLine in dataArray:
    if len(eachLine) > 1 and eachLine[0].isdigit():
        dataLine = eachLine.split(',')
        mainsArray.append(dataLine)

for row in range(7):
    for eachLine in mainsArray:
        if int(eachLine[0]) == int(datetime.strftime(dateList[row],'%j')):
            mainsTemp = float(eachLine[1])
    for col in range(24):
        enData[row][col] = volData[row][col] * (120 - mainsTemp)*2.44/1000
        

fig1 = plt.figure()
x1 = range(24)
daynames = []
dailyTotalEn = zeros(7)
maxIndex = unravel_index(enData.argmax(), enData.shape)
maxEntry = enData[maxIndex]
for row in range(7):
    fig1.add_subplot(2,4,row+1)
    plt.bar(x1,enData[row])
    plt.axis([0,23,0,maxEntry])
    plt.xticks(range(24)[0::2])
    plt.ylabel('Energy Consumption (kWh)')
    plt.xlabel('Hour of Day')
    plt.title(datetime.strftime(dateList[row], '%A, %m-%d-%Y'))
    dailyTotalEn[row] = sum(enData[row])
    daynames.append(datetime.strftime(dateList[row],'%A'))
fig1.add_subplot(2,4,8)
x2 = range(1,8)
plt.bar(x2,dailyTotalEn)
plt.xticks(x2, daynames)
plt.xticks(rotation=45)
plt.title('Total Energy Consumption by Day')
plt.ylabel('Energy Consumption (kWh)')
plt.xlabel('Day of Week')


fig2 = plt.figure()
fig2.add_subplot(1,1,1)
plt.axis([0,23,0,1])
plt.bar(x1,enData[3])
plt.xticks(range(24)[0::2])
plt.ylabel('Energy Consumption (kWh)')
plt.xlabel('Hour of Day')
plt.title(datetime.strftime(dateList[3], '%A, %m-%d-%Y'))
fig3 = plt.figure()
fig3.add_subplot(1,1,1)
plt.bar(x2,dailyTotalEn)
plt.xticks(x2, daynames)
plt.xticks(rotation=45)
plt.title('Total Energy Consumption by Day')
plt.ylabel('Energy Consumption (kWh)')
plt.xlabel('Day of Week')
plt.show()

