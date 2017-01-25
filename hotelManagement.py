import sqlite3
import os
import sys
import os.path

cronhoteldb = [None]


def main(args):
    # if db file exist than exit
    if os.path.isfile('cronhoteldb.db'):
        exit()  # maybe quit()

    else:
        # with open(args[1], 'r') as configFile:
        createDB()
        insertConfigToDB(args[1])
        cronhoteldb.close()


def createDB():
    global cronhoteldb
    cronhoteldb = sqlite3.connect('cronhoteldb.db')
    with cronhoteldb:
        cursor = cronhoteldb.cursor()

        cursor.execute("""CREATE TABLE TaskTimes
                        (TaskId INTEGER PRIMARY KEY NOT NULL,
                        DoEvery INTEGER NOT NULL,
                        NumTimes INTEGER NOT NULL)""")

        cursor.execute("""CREATE TABLE Tasks
                        (TaskId INTEGER NOT NULL REFERENCES TaskTimes(TaskId),
                        TasksName TEXT NOT NULL, Parameter INTEGER)""")

        cursor.execute("""CREATE TABLE Rooms
                    (RoomNumber INTEGER PRIMARY KEY NOT NULL)""")

        cursor.execute("""CREATE TABLE Residents
                    (RoomNumber INTEGER NOT NULL REFERENCES Rooms(RoomNumber),
                    FirstName TEXT NOT NULL,
                    LastName TEXT NOT NULL )""")


def insertConfigToDB(config):
    with open(config, 'r') as configFile:
        taskId = 0
        for line in configFile:
            line = line[:-1]
            splitedLine = line.split(',')
            if splitedLine[0] == "room":
                addNewRoomToDB(splitedLine)
            else:
                addNewTaskToDB(splitedLine, taskId)
                taskId += 1
    configFile.close()
    cronhoteldb.commit()


def addNewRoomToDB(roomLine):
    cursor = cronhoteldb.cursor()
    roomNumber = roomLine[1]
    cursor.execute("""INSERT INTO Rooms VALUES(?)""", (roomNumber,))
    if len(roomLine) == 4:
        firstName = roomLine[2]
        lastName = roomLine[3]
        cursor.execute("""INSERT INTO Residents VALUES (?,?,?)""", (roomNumber, firstName, lastName,))

def addNewTaskToDB(taskLine, taskId):
    cursor = cronhoteldb.cursor()
    taskName = taskLine[0]
    doEvery = taskLine[1]
    if len(taskLine) == 4:
        roomNumber = taskLine[2]
        numberTimes = taskLine[3]
    else:
        numberTimes = taskLine[2]
        roomNumber = 0
    cursor.execute("""INSERT INTO TaskTimes VALUES (?,?,?)""", (taskId, doEvery, numberTimes,))
    cursor.execute("""INSERT INTO Tasks VALUES (?,?,?)""", (taskId, taskName, roomNumber,))


if __name__ == '__main__':
    main(sys.argv)
