# mysql_functions.py 
# author: Maroua EL imame
# This file stores the MySQL menu option functions.


from db_connect import get_mysql_connection


# function for option 1 in menu to view speakers & sessions

def view_speakers():
    name = input("Enter speaker name : ")

    conn = get_mysql_connection()
    cursor = conn.cursor()
    # SQL query retrieves speaker name, session title, and room, filtering results based on a partial match of the speaker's name using the LIKE operator.
    query = """SELECT s.speakerName, s.sessionTitle, r.roomName
    FROM session s
    JOIN room r ON s.roomid = r.roomid
    WHERE s.speakerName LIKE %s
    ORDER BY s.speakerName
    """

    cursor.execute(query, ("%" + name + "%",))
    rooms_cache = cursor.fetchall()

    print("\nSession Details For :", name)
    print("-----------------------------------")

    if rooms_cache:
        for speaker, session, room in rooms_cache:
            print(f"{speaker:<20} | {session:<30} | {room}")
    else:
        print("No speakers found of that name")

    conn.close()




# function for option 2 in menu to view attendees by company

def view_attendees_by_company():
    # validate company ID input (must be a positive integer)
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

    # check if company exists in database
    company_query = """
    SELECT companyName
    FROM company
    WHERE companyID = %s
    """

    cursor.execute(company_query, (company_id,))
    company_result = cursor.fetchone()

    # if no company is found, display error and return to menu
    if not company_result:
        print(f"Company with ID {company_id} doesn't exist")
        conn.close()
        return

    company_name = company_result[0]

    # retrieve attendees and their session details using table joins
    query = """
    SELECT 
        a.attendeeName, a.attendeeDOB,
        s.sessionTitle, s.speakerName, s.sessionDate,
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

    # if the query returns rows, loop through them and display each result.

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
    # clean user input by removing extra spaces (.strip)
    attendee_id = input("Attendee ID : ").strip()
    name = input("Name : ").strip()
    dob = input("DOB : ").strip()
    gender = input("Gender : ").strip()
    company_id = input("Company ID : ").strip()

    conn = get_mysql_connection()
    cursor = conn.cursor()

    # check if attendee ID already exists in database
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

    # validate gender input  
    if gender not in ["Male", "Female"]:
        print("*** ERROR *** Gender must be Male/Female")
        cursor.close()
        conn.close()
        return

    # check if company ID exists in database  
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

    # insert  new attendee record into database using parameterized query to prevent SQL injection
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




# function for option 6 in menu to view rooms

# load room data once and reuse it (simple caching)

rooms_cache = None

def view_rooms():
    global rooms_cache

    if rooms_cache is None:
        conn = get_mysql_connection()
        cursor = conn.cursor()

        query = """
        SELECT roomID, roomName, capacity
        FROM room
        ORDER BY roomID
        """

        cursor.execute(query)
        rooms_cache = cursor.fetchall()

        cursor.close()
        conn.close()

    print("\nRooms")
    print("------")

    if rooms_cache:
        print(f"{'RoomID':<8} | {'RoomName':<20} | {'Capacity'}")
        print("-" * 45)

        for room_id, room_name, capacity in rooms_cache:
            print(f"{room_id:<8} | {room_name:<20} | {capacity}")

    else:
        print("No rooms found")





# function for option 7 in menu to generate an attendance report
# it combines MySQL aggregation, matplotlib graphing, and ReportLab PDF export


def generate_attendance_by_room_report():

    import matplotlib.pyplot as plt

    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import (
        SimpleDocTemplate,
        Paragraph,
        Spacer,
        Table,
        TableStyle,
        Image
    )

    from reportlab.lib import colors

    from reportlab.lib.styles import (
        getSampleStyleSheet,
        ParagraphStyle
    )

    from reportlab.lib.enums import TA_CENTER

    # gnerated files are saved in the project root folder
    pdf_file = "generated_attendance_report.pdf"
    graph_file = "generated_attendance_graph.png"

    conn = get_mysql_connection()
    cursor = conn.cursor()

    # SQL query joins room, session, and registration tables
    # COUNT is used to calculate registered attendees per session
    # available seats are calculated from room capacity
    query = """
    SELECT
        r.roomName,
        s.sessionTitle,
        s.speakerName,
        s.sessionDate,
        r.capacity,
        COUNT(reg.registrationID) AS registered_attendees,
        (r.capacity - COUNT(reg.registrationID)) AS available_seats

    FROM room r

    JOIN session s
    ON r.roomID = s.roomID

    LEFT JOIN registration reg
    ON s.sessionID = reg.sessionID

    GROUP BY
        r.roomName,
        s.sessionTitle,
        s.speakerName,
        s.sessionDate,
        r.capacity

    ORDER BY registered_attendees DESC;
    """

    cursor.execute(query)

    results = cursor.fetchall()

    cursor.close()
    conn.close()

    if not results:
        print("*** ERROR *** No attendance data found")
        return

    print("\nAttendance by Room Report")
    print("-------------------------")

    print(
        f"{'Room':<20} | "
        f"{'Session':<40} | "
        f"{'Speaker':<22} | "
        f"{'Date':<12} | "
        f"{'Capacity':<10} | "
        f"{'Registered':<12} | "
        f"{'Available'}"
    )

    print("-" * 150)

    for room, session, speaker, session_date, capacity, registered, available in results:

        print(
            f"{room:<20} | "
            f"{session:<40} | "
            f"{speaker:<22} | "
            f"{str(session_date):<12} | "
            f"{capacity:<10} | "
            f"{registered:<12} | "
            f"{available}"
        )

    # calculate attendance percentage for graph
    # formula: (registered attendees / room capacity) * 100
    labels = [row[1] for row in results]

    attendance_percentages = [
        (row[5] / row[4]) * 100
        for row in results
    ]
    # create and save attendance percentage bar chart
    plt.figure(figsize=(12, 6))

    plt.bar(
        labels,
        attendance_percentages,
        color="plum"
    )

    plt.grid(
        axis="y",
        linestyle="--",
        alpha=0.6
    )

    plt.xlabel("Session")

    plt.ylabel("Attendance Percentage (%)")

    plt.title("Generated Attendance Percentage Report")

    plt.xticks(rotation=45, ha="right")

    plt.tight_layout()

    plt.savefig(graph_file)

    plt.close()

    # calculations

    highest = max(results, key=lambda row: row[5])

    lowest = min(results, key=lambda row: row[5])

    highest_percentage = max(
        results,
        key=lambda row: (row[5] / row[4]) * 100
    )

    highest_percent_value = (
        highest_percentage[5] / highest_percentage[4]
    ) * 100

    total_registered = sum(row[5] for row in results)

    average_attendance = total_registered / len(results)

    # dfine PDF text styles and alignment  

    styles = getSampleStyleSheet()

    center_title_style = ParagraphStyle(
        name="CenterTitle",
        parent=styles["Heading2"],
        alignment=TA_CENTER
    )

    center_body_style = ParagraphStyle(
        name="CenterBody",
        parent=styles["BodyText"],
        alignment=TA_CENTER
    )

    # build PDF report structure

    doc = SimpleDocTemplate(
        pdf_file,
        pagesize=A4
    )

    content = []

    # title

    content.append(
        Paragraph(
            "Conference Attendance Report",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 12))

    # intro

    intro = """
    This report uses live registration data from the up-to-date database
    to show registered attendees, room capacity, available seats,
    and room attendance percentage.
    """

    content.append(
        Paragraph(
            intro,
            center_body_style
        )
    )

    content.append(Spacer(1, 18))

    # create attendance table for PDF

    table_data = [[
        "Room",
        "Session",
        "Speaker",
        "Date",
        "Capacity",
        "Registered",
        "Available"
    ]]

    for row in results:

        table_data.append([
            row[0],
            row[1],
            row[2],
            str(row[3]),
            row[4],
            row[5],
            row[6]
        ])

    table = Table(
        table_data,
        repeatRows=1
    )

    table.setStyle(TableStyle([

        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),

        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),

        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

        ("ALIGN", (4, 1), (-1, -1), "CENTER"),

        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

    ]))

    content.append(table)

    content.append(Spacer(1, 20))

    # add generated graph image to PDF

    content.append(
        Paragraph(
            "Attendance Percentage Graph",
            center_title_style
        )
    )

    content.append(
        Image(
            graph_file,
            width=480,
            height=300
        )
    )

    content.append(Spacer(1, 18))

    # analysis section

    content.append(
        Paragraph(
            "Automatic Analysis",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            f"The session with the highest number of registered attendees is "
            f"{highest[1]} in {highest[0]}, "
            f"with {highest[5]} registered attendees.",
            styles["BodyText"]
        )
    )
    # vertical space between PDF elements
    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            f"The session with the lowest number of registered attendees is "
            f"{lowest[1]} in {lowest[0]}, "
            f"with {lowest[5]} registered attendees.",
            styles["BodyText"]
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            f"The highest room attendance percentage is for "
            f"{highest_percentage[1]} in {highest_percentage[0]}, "
            f"with {highest_percent_value:.2f}% room occupancy.",
            styles["BodyText"]
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            f"The total number of registered attendances across all sessions is "
            f"{total_registered}.",
            styles["BodyText"]
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            f"The average attendance per session is "
            f"{average_attendance:.2f} attendees.",
            styles["BodyText"]
        )
    )

    # generate final PDF file

    doc.build(content)

    print(f"\nPDF report created successfully: {pdf_file}")
    print(f"Graph image created successfully: {graph_file}")
    print("Open the project folder to view the generated files.\n")
    print("For more details about the reporting feature, please refer to innovation.pdf")