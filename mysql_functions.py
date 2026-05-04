# mysql_functions.py 
# This file stores the MySQL menu option functions.


from db_connect import get_mysql_connection


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








# function for option 2 in menu to view attendees by company
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






# function for option 3 in menu to add new attendee
def add_new_attendee():
    print("\nAdd New Attendee")
    print("----------------")

    attendee_id = input("Attendee ID : ").strip()
    name = input("Name : ").strip()
    dob = input("DOB : ").strip()
    gender = input("Gender : ").strip()
    company_id = input("Company ID : ").strip()

    conn = get_mysql_connection()
    cursor = conn.cursor()

    # Check if attendee ID already exists
    attendee_check_query = """
    SELECT attendeeID
    FROM attendee
    WHERE attendeeID = %s
    """

    cursor.execute(attendee_check_query, (attendee_id,))
    attendee_result = cursor.fetchone()

    if attendee_result:
        print(f"*** ERROR *** Attendee ID: {attendee_id} already exists")
        cursor.close()
        conn.close()
        return

    # Check that gender is valid
    if gender not in ["Male", "Female"]:
        print("*** ERROR *** Gender must be Male/Female")
        cursor.close()
        conn.close()
        return

    # Check if company ID exists
    company_check_query = """
    SELECT companyID
    FROM company
    WHERE companyID = %s
    """

    cursor.execute(company_check_query, (company_id,))
    company_result = cursor.fetchone()

    if not company_result:
        print(f"*** ERROR *** Company ID: {company_id} does not exist")
        cursor.close()
        conn.close()
        return

    # Insert the new attendee
    insert_query = """
    INSERT INTO attendee
    (attendeeID, attendeeName, attendeeDOB, attendeeGender, attendeeCompanyID)
    VALUES (%s, %s, %s, %s, %s)
    """

    try:
        cursor.execute(insert_query, (attendee_id, name, dob, gender, company_id))
        conn.commit()
        print("\nAttendee successfully added")

    except Exception as e:
        print("*** ERROR ***", e)
        

    cursor.close()
    conn.close()




    # 