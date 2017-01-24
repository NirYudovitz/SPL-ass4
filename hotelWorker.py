import time
import sqlite3

cronhoteldb = [None]


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
    print firstName + " " + lastName + " in room " + roomNumber + " received a wakeup call at " + time.time()

def eatbreakfast(roomNumber):
    pass


def cleanSomeRooms():
    pass


def getResidentName(roomNumber):
    cronhoteldb = sqlite3.connect('cronhoteldb.db')
    cursor = cronhoteldb.cursor()
    cursor.execute("SELECT FirstName, LastName FROM Residents WHERE RoomsNumber = (?)", (roomNumber,))
    return cursor.fetchone()
