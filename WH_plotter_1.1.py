import matplotlib.pyplot as plt
import matplotlib.animation as animation

#Initialize plot figure
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

#Define function to animate plot
def animate(i):
    pullData = open('Waterheater_Data.csv','r').read()
    dataArray = pullData.split('\n')
    xar = []
    yar = []
    for eachLine in dataArray:
        if len(eachLine)>1:
            date,time,temp,hour = eachLine.split(',')
            if temp[0].isdigit():
                xar.append(float(hour))
                yar.append(float(temp))
        ax1.clear()
        plt.xlabel('Hour of Day')
        plt.ylabel('Water Temperature (Degrees F)')
        plt.title('Water Heater Measurements')
        ax1.plot(xar,yar)
ani = animation.FuncAnimation(fig,animate, interval=30000)
plt.show()
