
# import required libraries to connect Python to MySQL
import mysql.connector


# Display main menu with options for the user to choose from

def show_menu():
    print("\nConference Management")
    print("---------------------")
    print()
    print("MENU")
    print("====")
    print("1 - View Speakers & Sessions")
    print("2 - View Attendees by Company")
    print("3 - Add New Attendee")
    print("4 - View Connected Attendees")
    print("5 - Add Attendee Connection")
    print("6 - View Rooms")
    print("x - Exit application")


# function for option 1 in menu to view speakers & sessions  

def view_speakers():
    name = input("Enter speaker name : ")

    # establish connection to MySQL database

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="yourpassword",  
        database="appdbproj"
    )

    cursor = conn.cursor()

    query = """
    SELECT s.name, se.title, r.name
    FROM speaker s
    JOIN session se ON s.id = se.speaker_id
    JOIN room r ON se.room_id = r.id
    WHERE s.name LIKE %s
    """

    # execute the query using user input ( allowing for partial matches)
    cursor.execute(query, ("%" + name + "%",))
    results = cursor.fetchall()

    # print header  
    print("\nSession details for :", name)
    print("-----------------------------------")

    # Loop through each row in the result set. :< string formatting is used to align output in a tabular format. 
    # https://docs.python.org/3/library/string.html#:~:text=align%3A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%22%3C%22%20%7C%20%22%3E%22%20%7C%20%22%3D%22%20%7C%20%22%5E%22
     
    for speaker, session, room in results:
        print(f"{speaker:<20} | {session:<30} | {room}")

    conn.close()

# COMING NEXT: functions for options 2-6 in menu

#def view_attendees_by_company(): 

#def add_attendee():

#def view_connected_attendees():

#def add_attendee_connection():

#def view_rooms():

#######

# Run on main  

while True:
    show_menu()
    choice = input("Choice: ").lower() # only accept lowercase input for easier handling of 'x' to exit

    if choice == "1":
        view_speakers()

    elif choice == "2":
    # next implement attendees by company (SQL query + display)
        print("\n[Coming next] View Attendees by Company\n")

    elif choice == "3":
        print("\n[Coming next] Add New Attendee\n")

    elif choice == "4":
        print("\n[Coming next] View Connected Attendees\n")

    elif choice == "5":
        print("\n[Coming next] Add Attendee Connection\n")  

    elif choice == "6":
        print("\n[Coming next] View Rooms\n")

    elif choice == "x":
        print("\nExiting application...")
        break

    else:
        print("\nInvalid choice. Please enter a number from 1 to 6, or x to exit.")