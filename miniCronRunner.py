import os
import time
import sqlite3

cronhoteldb = [None]




def main():
    global cronhoteldb
    cronhoteldb = sqlite3.connect('cronhoteldb.db')
    tasksRemain = countTasks()
    while os.path.isfile('cronhoteldb.db') and tasksRemain>0:
        taskValues = getTaskValues()


def getTaskValues():
    cronhoteldb = sqlite3.connect('cronhoteldb.db')
    cursor = cronhoteldb.cursor()
    cursor.execute("SELECT * FROM TaskTimes WHERE NumTimes > 0")


def countTasks():
    cursor = cronhoteldb.cursor
    cursor.execute("SELECT NumTimes FROM TaskTimes")
    sum = 0
    for row in cursor.fetchall():
        sum += int(row[0])
    return sum

if __name__ == '__main__':
    main()
