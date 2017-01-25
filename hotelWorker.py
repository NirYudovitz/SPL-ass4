import time
import sqlite3

cronhoteldb = sqlite3.connect('cronhoteldb.db')


def dohoteltask(taskname, parameter):
    if taskname == "wakeup":
        performWakeup(parameter)
    elif taskname == "breakfast":
        eatbreakfast(parameter)
    elif taskname == "clean":
        cleanSomeRooms()


def performWakeup(roomNumber):
    resident = getResidentName(roomNumber)
    firstName = resident[0]
    lastName = resident[1]
    print firstName + " " + lastName + " in room " + str(roomNumber) + " received a wakeup call at " + str(time.time())
    return time.time()

def eatbreakfast(roomNumber):
    resident = getResidentName(roomNumber)
    firstName = resident[0]
    lastName = resident[1]
    print firstName + " " + lastName + " in room " + str(roomNumber) + " has been served breakfast at " + str(time.time())
    return float(time.time())

def cleanSomeRooms():
    cursor = cronhoteldb.cursor()
    cursor.execute("""SELECT roomNumber FROM rooms WHERE roomNumber NOT IN (SELECT roomNumber FROM Residents)
                    ORDER BY roomNumber ASC""")
    emptyRooms = ""
    for row in cursor.fetchall():
        emptyRooms += str(row[0]) + ", "
    emptyRooms = emptyRooms[:-2]
    print "Rooms " + emptyRooms + " were cleaned at " + str(time.time())
    return float(time.time())

def getResidentName(roomNumber):
    cursor = cronhoteldb.cursor()
    cursor.execute("""SELECT FirstName, LastName FROM Residents WHERE RoomNumber = (?)""", (roomNumber,))
    return cursor.fetchone()
