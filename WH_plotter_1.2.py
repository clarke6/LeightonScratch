import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.dates as mdates
import datetime

#Initialize plot figure
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

#Define function to animate plot
def animate(i):
    now = datetime.datetime.now()
    filename = 'WH_Data_' + str(now.month) + '-' + str(now.day) + '-' + str(now.year) + '.csv'
    pullData = open(filename,'r').read()
    dataArray = pullData.split('\n')
    xar = []
    yar = []
    for eachLine in dataArray:
        if len(eachLine)>1:
            time,temp = eachLine.split(',')
            if temp[0].isdigit():
                time = datetime.datetime.strptime(time, '%H:%M')
                xar.append(time)
                yar.append(float(temp))
        ax1.clear()
        plt.xlabel('Time of Day')
        plt.ylabel('Water Temperature (Degrees F)')
        plt.title('Water Heater Measurements: %g-%g-%g' % (now.month, now.day, now.year))
        ax1.plot(xar,yar)
        plt.gcf().autofmt_xdate()
        myFmt = mdates.DateFormatter('%H:%M')
        ax1.xaxis.set_major_formatter(myFmt)
ani = animation.FuncAnimation(fig,animate, interval=30000)
plt.show()
