import time as t
from random import shuffle
import sqlite3

def sql_insert(con, event): 
    cursorObj = con.cursor()

    cursorObj.execute('''INSERT INTO events(event, year) VALUES(?, ?)''', event)   
    con.commit()
    
def add_event(con):
    event = input("Enter an event that took place between A.D. 1750 and 2023. ")
    year = input("Enter the year this event took place: ")
    event = (event, year)
    sql_insert(con, event)

def sql_fetch(con):
    cursorObj = con.cursor()
    cursorObj.execute('SELECT * FROM events')
    rows = cursorObj.fetchall()
    for x, y in rows:
        eventMap[x] = y
    print(eventMap)

def del_event(con):
    delEvent =input("Which event would you like to delete? ")
    cursorObj = con.cursor()
    query = 'DELETE FROM events WHERE event=?'
    cursorObj.execute(query, (delEvent,))
    con.commit()
    
con = sqlite3.connect('years.db')

addEvent = input("Would you like to add an event to the database? y/n ") 
while (addEvent.upper()) != "Y" and (addEvent.upper()) != "N":
     addEvent = input("\nWhoops! Invalid entry, type 'y' or 'no' please. \n")
while (addEvent.upper()) == "Y":
    add_event(con)
    addEvent = input("Would you like to add another event? y/n \n")
    while (addEvent.upper()) != "Y" and (addEvent.upper()) != "N":
        addEvent = input("Whoops! Invalid entry, type 'y' or 'n' please. \n")

delEvent = input("Would you like to delete an event from the database? y/n ")
while (delEvent.upper()) != "Y" and (delEvent.upper()) != "N":
    delEvent = input("\nWhoops! Invalid entry, type 'y' or 'no' please. \n")
while (delEvent.upper()) == "Y":
    del_event(con)
    delEvent = input("Would you like to delete another event? y/n \n")
    while (delEvent.upper()) != "Y" and (delEvent.upper()) != "N":
        delEvent = input("Sorry, invalid entry. Please type 'y' or 'n' please. \n")
        
eventMap = {}
sql_fetch(con)

eventList = [] # Creates a list
for event in eventMap: # Populates list with keys from the above dict
    eventList.append(event)
shuffle(eventList) # Randomizes the list

randomEventsMap = {} # Creates new dict using randomized list
for event in eventList:
    randomEventsMap[event]=(eventMap[event])
        
streak = 0
print('\nWelcome to "Years"\n')
t.sleep(2)
difficulty = input('''Choose your difficulty level:
A) Easy
B) Moderate
C) Hard
D) Impossible

''')
while True:
    if (difficulty.upper()) == "A":
        score = 1000
        break
    elif (difficulty.upper()) == "B":
        score = 500
        break
    elif (difficulty.upper()) == "C":
        score = 100
        break
    elif (difficulty.upper()) == "D":
        score = 1
        break
    else:
        difficulty = input("Invalid selection. Please choose 'A', \
'B', 'C', or 'D': ")

for event in randomEventsMap:
    if score <=0:
        break
    else: 
        if streak == 0:
            print("Beginning score: %d\n" % score)
        else:
            print("\nScore: " + str(score) + "\n")
        t.sleep(2)
        guessesUsed = 0
        print(event)
        yearGuess = int(input("Guess the year: \n----\n"))
        correctAnswer = False
        while correctAnswer == False:
            if score <= 0:
                break
            if type(yearGuess) == int and len(str(yearGuess)) == 4:
                if yearGuess == eventMap[event]:
                    streak+=1
                    print("Correct!\nStreak: " + str(streak))
                    t.sleep(2)
                    correctAnswer = True
                else:
                    guessesUsed+=1
                    score -= guessesUsed * abs(randomEventsMap[event] - yearGuess)
                    if score > 0:
                        for i in range (0, 4):
                            if str(yearGuess)[i] == str(randomEventsMap[event])[i]:
                                print(str(randomEventsMap[event])[i], end="")
                                t.sleep(0.75)
                            else:
                                print("-", end="")
                                t.sleep(0.75)
                        yearGuess = int(input("\n"))
                    else:
                        print("The correct answer is: " + str(randomEventsMap[event]))
            else:
                 yearGuess = int(input("Please enter a four digit year: \n"))
print("\nGame over.\n")
t.sleep(2)
print("Final streak: " + str(streak))                
