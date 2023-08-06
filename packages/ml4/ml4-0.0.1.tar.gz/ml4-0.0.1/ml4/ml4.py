#Wikicivi Crawler Client SDK
import numpy as np


class ml4:
    def __init__(self):
        self.apimap = {}
    

    #LOG,INFO,WARN,ERROR,
    def intro():
        print("这是TechYoung课程的机器学习辅助工具包")
        return True

    def getWindowData(data, x, y, windowSize=300, steps=300):
        data = np.array(data[[y, x]])

        timeStart = data[0, 1]
        timeEnd = data[-1, 1]

        infoList = []
        for windowStart in range(timeStart, timeEnd, steps):
            windowEnd = windowStart - windowSize
            for j in range(len(data)):
                if windowEnd < data[j, 1] <= windowStart:
                    infoList.append([data[j, 0], windowEnd])
                elif data[j, 1] > windowStart:
                    break
            windowStart += steps
        infoList = np.array(infoList)
        return infoList[:, 1], infoList[:, 0]