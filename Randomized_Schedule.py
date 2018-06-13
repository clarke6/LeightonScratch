from datetime import datetime
from numpy.random import normal
from numpy import zeros
import random
import matplotlib.pyplot as plt

events = zeros((24,60))
hourlySums = zeros(24)

for hour in range(24):
    if hour < 6 or hour > 22:
        numEvents = int(normal(5,2))
        drawSize = 0.2
        drawSD = 0.05
    elif hour >= 5 and hour < 12:
        numEvents = int(normal(10,5))
        drawSize = 0.75
        drawSD = 0.5
    elif hour >=12 and hour < 17:
        numEvents = int(normal(7,2))
        drawSize = 0.25
        drawSD = 0.1
    elif hour >=17 and hour < 22:
        numEvents = int(normal(15,5))
        drawSize = 0.5
        drawSD = 0.3
    if numEvents > 0:
        minutes = random.sample(range(60),numEvents)
    else:
        numEvents = 0

    for event in range(numEvents):
        eventSize = normal(drawSize,drawSD)
        if eventSize > 0:
            events[hour][minutes[event]] = eventSize

    hourlySums[hour] = sum(events[hour])

plt.bar(range(24),hourlySums)
plt.show()
