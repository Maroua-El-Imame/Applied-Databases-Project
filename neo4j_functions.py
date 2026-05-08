# neo4j_functions.py
# Author: Maroua EL imame
# This file stores the Neo4j menu option functions.


from db_connect import get_neo4j_driver
from db_connect import get_mysql_connection

# function for option 4 in menu to view connected attendees
def view_connected_attendees():
    attendee_id = input("\nEnter Attendee ID: ")

    if not attendee_id.isdigit():
        print("*** ERROR *** Invalid attendee ID")
        return

    attendee_id = int(attendee_id)

    conn = get_mysql_connection()
    cursor = conn.cursor()

    query = """
    SELECT attendeeName
    FROM attendee
    WHERE attendeeID = %s
    """

    cursor.execute(query, (attendee_id,))
    mysql_row = cursor.fetchone()

    cursor.close()
    conn.close()

    if not mysql_row:
        print("*** ERROR *** Attendee does not exist")
        return

    attendee_name = mysql_row[0]

    driver = get_neo4j_driver()

    with driver.session() as session:
        result = session.run( 
            """
            MATCH (a:Attendee {AttendeeID: $attendee_id})
            OPTIONAL MATCH (a)-[:CONNECTED_TO]-(connected:Attendee)
            RETURN collect(connected.AttendeeID) AS connections
            """,
            attendee_id=attendee_id
        )
        record = result.single()

        print(f"Attendee ID: {attendee_id}")
        print(f"Attendee Name: {attendee_name}")
        print("--------------------")

        if record is None:
            print("No connections")
            return

        connections = record["connections"]

        if not connections:
            print("No connections")
        else:
            print("These attendees are connected:")
            for person in connections:
                print(person)













# COMING NEXT:
# def add_attendee_connection():