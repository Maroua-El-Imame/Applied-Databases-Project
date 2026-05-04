# main.py 
# Author: Maroua EL imame

# This is the main file of the conference management application. 
# menu / user choices only

import db_connect

from mysql_functions import (
    view_speakers,
    view_attendees_by_company,
    add_new_attendee,
)
from db_connect import get_neo4j_driver


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




# Next : 
#def view_connected_attendees():

#def add_attendee_connection():

#def view_rooms():

#------------------------------------------------


# Run main application  

while True:
    show_menu()
    choice = input("Choice: ").lower() 

    if choice == "1":
        view_speakers()

    elif choice == "2":
        view_attendees_by_company()

    elif choice == "3":
        add_new_attendee()

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