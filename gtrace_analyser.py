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


N = 10

tDict = dict()
tNum = -1
tfNum = 0
tName = ""
sTime = 0
tList = list()
fo = open("Input", "w")

for i in xrange(0, N):
    file_path = "/Users/Oceans/Git/Google-trace/task_events/part-%05d-of-00500.csv" % (i)
    with open(file_path, 'rb') as fi:
        lines = csv.reader(fi)
        for l in lines:
            tName = l[2] + l[3]
            tType = l[5]
            tTime = int(l[0])
            if tTime == 0: continue
            if (tTime - sTime) / 1000000  > 5 * 60 * 60: break
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

cMax = 0
mMax = 0
dMax = 0
tList.sort()
j = 0

for i in tList:
    if i.status == 1:
        if random.random() <= 0.12:
            tStart = (i.s_time - sTime) / 1000000
            tDuration = (i.f_time - i.s_time) / 1000000
            # if tDuration > 5000: continue

            j += 1
            cMax = max(cMax, i.r_cpu)
            mMax = max(mMax, i.r_mem)
            dMax = max(dMax, tDuration)
            fo.write("%d %d %d %d %d\n" % (j, tStart, tDuration , max(int(math.ceil(i.r_cpu * 100)),1)  , max(int(math.ceil(i.r_mem * 100)),1)))

fo.close()
print tNum
print tfNum
print cMax, mMax, dMax
