# 1. timestamp
# 2. missing info
# 3. job ID
# 4. task index - within the job
# 5. machine ID
# 6. event type
# 7. user name
# 8. scheduling class
# 9. priority
# 10. resource request for CPU cores
# 11. resource request for RAM
# 12. resource request for local disk space
# 13. different-machine constraint



import csv
import sys
import os
import math
import random

class TaskInfo(object):
    def __init__(self, id = 0, s_time = 0, f_time = 0, r_cpu = 0.0, r_mem = 0.0, status = 0):
        self.id = id
        self.s_time = s_time
        self.f_time = f_time
        self.r_cpu = r_cpu
        self.r_mem = r_mem
        self.status = status

    def __lt__(self, other):
        return self.s_time < other.s_time


N = 0
H = 5 * 60 * 60
R = 1
K = 400

tDict = dict()
tNum = -1
tfNum = 0
tName = ""
sTime = sys.maxint
tList = list()
fo = open("Input", "w")

for i in xrange(N, N + 20):
    file_path = "/Users/Oceans/Git/Google-trace/task_events/part-%05d-of-00500.csv" % (i)
    with open(file_path, 'rb') as fi:
        lines = csv.reader(fi)
        for l in lines:
            tName = l[2] + l[3]
            tType = l[5]
            tTime = int(l[0])
            if tTime == 0: continue
            if (tTime - sTime) / 1000000  > H: break
            tCpu = float(l[9])
            tMem = float(l[10])

            if tType == '0':
                if tDict.has_key(tName):
                    j = tDict[tName]
                    if tList[j].status != 1:
                        tList[j].s_time = tTime
                        tList[j].r_cpu = tCpu
                        tList[j].r_mem = tMem
                        tList[j].status = 0
                else:
                    tNum += 1
                    if tNum == 0: sTime = tTime
                    tDict[tName] = tNum
                    tList.append(TaskInfo(tNum, tTime, 0, tCpu, tMem, 0))

            if tType == '4':
                if tDict.has_key(tName):
                    j = tDict[tName]
                    if tList[j].status == 0:
                        tfNum += 1
                        tList[j].f_time = tTime
                        tList[j].status = 1
    fi.close()

tList.sort()

jobNum = 0

sumDuration = 0.0
sumCpu = 0.0
sumMem = 0.0

maxDuration = 0
maxCpu = 0
maxMem = 0

usageCpu = 0.0
usageMem = 0.0
for i in tList:
    if i.status == 1:
        if random.random() <= R:
            tStart = (i.s_time - sTime) / 1000000
            tDuration = (i.f_time - i.s_time) / 1000000
            tCpu = max(int(math.ceil(i.r_cpu * K)),1)
            tMem = max(int(math.ceil(i.r_mem * K)),1)
            if tCpu > 50 or tMem > 50: continue
            # if tCpu <= 1 and tMem <= 1: continue
            # if tCpu == tMem: continue
            # if tDuration > 5000: continue

            jobNum += 1
            usageCpu += tCpu * tDuration
            usageMem += tMem * tDuration
            sumCpu += tCpu
            sumMem += tMem
            sumDuration += tDuration
            maxCpu = max(maxCpu, tCpu)
            maxMem = max(maxMem, tMem)
            maxDuration = max(maxDuration, tDuration)
            # fo.write("%d %d %d %d %d\n" % (jobNum, tStart, tDuration , tCpu, tMem))

fo.close()

avgCpu = sumCpu/jobNum
avgMem = sumMem/jobNum
avgDuration = sumDuration/jobNum


print "total jobs:", tfNum
print "select jobs:", jobNum
print "maxCpu:", maxCpu, " maxMem:", maxMem, "maxDuration:", maxDuration
print "avgCpu:", avgCpu, " avgMem:", avgMem, "avgDuration:", avgDuration
print "avgCpu Usage:", usageCpu / H / 1750
print "avgMem Usage:", usageMem / H / 1750
