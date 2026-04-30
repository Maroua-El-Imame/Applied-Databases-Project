
# import required libraries to connect Python to MySQL
import mysql.connector
from db_connect import get_mysql_connection


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

    conn = get_mysql_connection()
    cursor = conn.cursor()

    query = """SELECT s.speakerName, s.sessionTitle, r.roomName
    FROM session s
    JOIN room r ON s.roomid = r.roomid
    WHERE s.speakerName LIKE %s
    ORDER BY s.speakerName
    """

    cursor.execute(query, ("%" + name + "%",))
    results = cursor.fetchall() 

    print("\nSession Details For :", name)
    print("-----------------------------------")

    if results:
        for speaker, session, room in results:
            print(f"{speaker:<20} | {session:<30} | {room}")
    else:
        print("No speakers found of that name")

    conn.close()


def view_attendees_by_company():
    # check if ID is valid (number greater than 0) and keep asking until valid input is given
    while True:
        try:
            company_id = int(input("Enter Company ID : "))

            if company_id > 0:
                break
            else:
                print("Invalid company ID ! Please enter a number greater than 0.")

        except ValueError:
                print("Invalid company ID ! Please enter a number greater than 0.")

    conn = get_mysql_connection()
    cursor = conn.cursor()

    # check if company exists  
    company_query = """
    SELECT companyName
    FROM company
    WHERE companyID = %s
    """

    cursor.execute(company_query, (company_id,))
    company_result = cursor.fetchone()

    # If no company is found, show an error message and stop the function, then return to ain menu. 
    if not company_result:
        print(f"Company with ID {company_id} doesn't exist")
        conn.close()
        return

    company_name = company_result[0]

    # Get all attendees from the selected company,

    query = """
    SELECT 
        a.attendeeName,a.attendeeDOB,
        s.sessionTitle,s.speakerName,s.sessionDate,
        r.roomName
    FROM attendee a
    JOIN registration reg ON a.attendeeID = reg.attendeeID
    JOIN session s ON reg.sessionID = s.sessionID
    JOIN room r ON s.roomID = r.roomID
    WHERE a.attendeeCompanyID = %s
    ORDER BY a.attendeeName
    """

    cursor.execute(query, (company_id,))
    results = cursor.fetchall()

    print(f"{company_name} Attendees")

    # If the query returns rows, loop through them and display each result.

    if results:
        for attendee, dob, session, speaker, session_date, room in results:
            print(f"{attendee:<15} | {dob} | {session:<30} | {speaker:<20} | {session_date} | {room}")
    else:
        print(f"No attendees found for {company_name}")

    conn.close()





# ------------------------------------------------

# COMING NEXT: functions for options 3-6 in menu

#def add_attendee():

#def view_connected_attendees():

#def add_attendee_connection():

#def view_rooms():

#------------------------------------------------


# Run on main  

while True:
    show_menu()
    choice = input("Choice: ").lower() 

    if choice == "1":
        view_speakers()

    elif choice == "2":
        view_attendees_by_company()

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