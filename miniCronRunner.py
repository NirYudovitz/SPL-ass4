import os
import sys
import os.path
import time
import sqlite3

cronhoteldb = [None]
idTimeMap = {}


def main():

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

            if taskId not in idTimeMap or (idTimeMap[taskId] + doEvery) <= time.time():
                import hotelWorker
                idTimeMap[taskId] = hotelWorker.dohoteltask(tasksName, parameter)
                tasksRemain -= 1
                decrement(taskId, numTimes)

    if os.path.isfile('cronhoteldb.db'):
        cronhoteldb.close()


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
    if os.path.isfile('cronhoteldb.db'):
        global cronhoteldb
        cronhoteldb = sqlite3.connect('cronhoteldb.db')
        cursor = cronhoteldb.cursor()
        cursor.execute("""SELECT NumTimes FROM TaskTimes""")
        sum = 0
        for row in cursor.fetchall():
            sum += int(row[0])
        return sum
    return 0

if __name__ == '__main__':
    main()
