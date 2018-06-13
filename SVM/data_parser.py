from numpy import zeros
import matplotlib.pyplot as plt

filename = raw_input('Enter name of file to read: ')
data = open(filename,'r').read()
dataArray = data.split('\n')
numdays = len(dataArray) / 2880
plotData = zeros((numdays,24))

row = 0
while row < len(dataArray):
    if len(dataArray[row]) > 1:
        dataLine = dataArray[row].split(',')
        if dataLine[4] == '3' and dataLine[6] == '1':
            day = (row) / 2880
            hour = ((row) - day * 2880) / 120
            plotData[day][hour] += 1
    row += 1

fig1 = plt.figure()
x1 = range(24)
x2 = range(1,8)
totalUsage = zeros(7)
for k in range(len(plotData)):
    fig1.add_subplot(2,4,k+1)
    plt.bar(x1,plotData[k])
    plt.title('Day ' + str(k+1))
    totalUsage[k] = sum(plotData[k])
fig1.add_subplot(2,4,8)
plt.bar(x2,totalUsage)
plt.title('Total Usage by Day')
plt.show()
