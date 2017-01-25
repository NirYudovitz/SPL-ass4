import os
import time
import sqlite3

import hotelWorker

cronhoteldb = sqlite3.connect('cronhoteldb.db')
idTimeMap = dict()

def main():
    global cronhoteldb
    tasksRemain = countTasks()
    while os.path.isfile('cronhoteldb.db') and tasksRemain > 0:
        cursor = getTaskValues()
        for row in cursor:
            taskId = row[0]
            tasksName = row[1]
            doEvery = row[2]
            numTimes = row[3]
            parameter = row[4]
            # print idTimeMap[taskId]

            if idTimeMap.get(taskId) is None or (idTimeMap[taskId] + doEvery) <= float(time.time()):
                idTimeMap[taskId] = float(hotelWorker.dohoteltask(tasksName, parameter))
                decrement(taskId, numTimes)
    cronhoteldb.close()
    exit()

def decrement(taskId, numTimes):
    cursor = cronhoteldb.cursor()
    cursor.execute("""UPDATE TaskTimes SET NumTimes=(?) WHERE TaskId=(?)""", [numTimes - 1, taskId])
    cronhoteldb.commit()

def getTaskValues():
    cursor = cronhoteldb.cursor()
    cursor.execute("""SELECT Tasks.TaskId, Tasks.TasksName, TaskTimes.DoEvery, TaskTimes.NumTimes, Tasks.Parameter
    FROM TaskTimes JOIN Tasks
    WHERE NumTimes > 0 AND
    Tasks.TaskId = TaskTimes.TaskId""")
    return cursor.fetchall()




def countTasks():
    cursor = cronhoteldb.cursor()
    cursor.execute("""SELECT NumTimes FROM TaskTimes""")
    sum = 0
    for row in cursor.fetchall():
        sum += int(row[0])
    return sum

if __name__ == '__main__':
    main()
