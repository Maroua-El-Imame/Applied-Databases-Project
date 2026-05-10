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

    driver.close()


# function for option 5 in menu to add attendee connection

def add_attendee_connection():
    attendee1_id = input("\nEnter Attendee 1 ID : ").strip()
    attendee2_id = input("Enter Attendee 2 ID : ").strip()

    # check numeric IDs
    if not attendee1_id.isdigit() or not attendee2_id.isdigit():
        print("*** ERROR *** Attendee IDs must be numbers")
        return

    attendee1_id = int(attendee1_id)
    attendee2_id = int(attendee2_id)

    # check attendee is not connecting to themselves
    if attendee1_id == attendee2_id:
        print("*** ERROR *** An attendee cannot connect to him/herself")
        return

    # check both attendees exist in MySQL
    conn = get_mysql_connection()
    cursor = conn.cursor()

    query = """
    SELECT attendeeID
    FROM attendee
    WHERE attendeeID IN (%s, %s)
    """

    cursor.execute(query, (attendee1_id, attendee2_id))
    mysql_results = cursor.fetchall()

    cursor.close()
    conn.close()

    if len(mysql_results) != 2:
        print("*** ERROR *** One or both attendee IDs do not exist")
        return

    driver = get_neo4j_driver()

    with driver.session() as session:

        # check if either attendee is already connected to anyone
        check_result = session.run(
            """
            MATCH (a:Attendee)
            WHERE a.AttendeeID IN [$attendee1_id, $attendee2_id]
            OPTIONAL MATCH (a)-[:CONNECTED_TO]-(:Attendee)
            RETURN count(*) AS total_nodes, count { (a)-[:CONNECTED_TO]-(:Attendee) } AS existing_connections
            """,
            attendee1_id=attendee1_id,
            attendee2_id=attendee2_id
        )

        record = check_result.single()

        if record["existing_connections"] > 0:
            print("*** ERROR *** These attendees are already connected")
            driver.close()
            return

        # create nodes if they do not already exist in Neo4j, then connect them
        session.run(
            """
            MERGE (a:Attendee {AttendeeID: $attendee1_id})
            MERGE (b:Attendee {AttendeeID: $attendee2_id})
            MERGE (a)-[:CONNECTED_TO]->(b)
            """,
            attendee1_id=attendee1_id,
            attendee2_id=attendee2_id
        )

        print(f"Attendee {attendee1_id} is now connected to Attendee {attendee2_id}")

    driver.close()









# COMING NEXT:
# def add_attendee_connection():