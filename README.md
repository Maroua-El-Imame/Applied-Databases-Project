# Conference Management Application - Project

Lecturer : Gerard Harrison  
Applied Databases S1-2026  
Higher Diploma in Science in Computing in Data Analytics  
Atlantic Technological University - ATU Galway Mayo 2025/2026.  

Author : Maroua EL imame  

Submission deadline : 13/05/2026  


<br/>
<br/>
<br/>



## Introduction  

This project is a command-line database application developed as part of the Applied Databases module.  
It allows users to interact with a conference management system using a menu-driven interface.  

The application connects to a MySQL database to retrieve and manage conference data such as speakers, sessions, attendees, and rooms.  
It also uses Neo4j to handle relationships between attendees.  

The goal of this project is to design and implement a database-driven application that integrates both relational and graph data models.  


## Table of Contents

- [Introduction](#introduction)
- [Folder Structure](#folder-structure)
- [Project Workflow](#project-workflow)
- [Environment Setup & App Running](#environment-setup--app-running)
- [Troubleshooting and Debugging Notes](#troubleshooting-and-debugging-notes)
- [Innovation](#innovation)
- [Contact](#contact)




## Folder Structure  
```text
Applied Databases Project/
│
├── main.py                  # Main menu and user choice logic
├── mysql_functions.py       # MySQL menu option functions
├── neo4j_functions.py       # Neo4j menu option functions
├── db_connect.py            # MySQL and Neo4j connection settings
├── requirements.txt         # Required Python packages
├── README.md                # Project overview and setup instructions
├── GitLink.txt              # GitHub repository link for submission
├── appdbproj.sql            # MySQL script creating appdbproj database, tables, relationships, and sample data
└── appdbprojNeo4j.json      # Neo4j script creating Attendee nodes and CONNECTED_TO relationships
```



## Project Workflow

The following workflow outlines the step-by-step process of this application based on a structured development approach.  
Each step was implemented progressively, with functionality added and tested throughout the project:

* [✔️] **Repository Setup**  
  Create the project repository and initial file structure.  

* [✔️] **Application Structure**  
  Organised the project into `main.py`, `mysql_functions.py`, `neo4j_functions.py`, and `db_connect.py`.  

* [✔️] **Menu Implementation**  
  Built the main command-line menu and connected user choices to the relevant functions  

- [✔️] **MySQL Feature Development**  
  Implemented MySQL-based features such as viewing speakers and sessions, viewing attendees by company, and adding new attendees.

- [✔️] **Input Validation and Error Handling**  
  Added validation for user input and handled cases such as invalid company IDs, missing companies, and empty query results.

- [✔️] **Neo4j Feature Preparation**  
  Added the Neo4j driver connection and prepared the project structure for graph-based attendee connection features.

- [✔️] **Testing**  
  Tested implemented options, database connections, menu flow, and VM compatibility.

- [ ] **Finalisation**  
  Complete remaining Neo4j features, final testing, documentation, and submission preparation.

 


## Environment Setup & App Running

Download and unzip the project folder.

1. Open the Project Folder

    Open **Cmder**, **Command Prompt**, or **PowerShell** in the project folder.  
      Example:

    ```cmd
      cd "C:\Users\appDB\Downloads\Applied Databases Project"
    ```
    <br>

    This project may require **three terminal windows** while testing:

- **Terminal 1:** MySQL shell — used to run SQL commands after logging into MySQL.
- **Terminal 2:** Run Neo4j server / Neo4j Browser — used for graph database setup and testing.
- **Terminal 3:** Run the Python application

<br>
   
3. Install required Python packages - These commands are run in the Command Prompt:
 
   ```bash
    pip install -r requirements.txt
    ```
    If package errors occur, update pip and reinstall the requirements:

    ```bash
      python -m pip install --upgrade pip
      python -m pip install -r requirements.txt
    ```

4. Ensure MySQL Server is running.
   ```bash
   net start MySQL80
    ```

5. Update database credentials in "db_connect.py".

   Update the MySQL and Neo4j username/password values so they match the local machine or VM.

   Example:
   ```bash
   MySQL - 
   password="YOUR_MYSQL_PASSWORD"
   Neo4j -
   auth=("neo4j", "YOUR_NEO4J_PASSWORD")
    ```

6. Set up the MySQL database  
    The file appdbproj.sql is already included in the project folder.


    Import the SQL database file:
    ```bash
      "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p < appdbproj.sql
    ```

    To verify that the database imported correctly, open MySQL:
    ```bash
      "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p    
      ```
    Then run the following commands inside the MySQL shell:

      ```sql
      SHOW DATABASES;
      USE appdbproj;
      SHOW TABLES;
      ```
    The conference management tables should now appear.  
    ```bash  
      +---------------------+  
      | Tables_in_appdbproj |  
      +---------------------+
      | attendee            |
      | company             |
      | registration        |
      | room                |
      | session             |
      +---------------------+
    ```

7. Set up Neo4j  
    Open 2nd Command Prompt and move into the Neo4j bin folder:
    ```bash
    cd "C:\Users\appDB\Documents\neo4j-community-5.26.19\bin"
    ```
    Start the Neo4j server:
    ```bash
    .\neo4j.bat console
    ```
    Leave this terminal window open while the application is running.

    When Neo4j starts successfully, the following message should appear:

    ```bash
    Remote interface available at http://localhost:7474/
    ```

    Neo4j Browser can then be accessed from:
    ```bash
    http://localhost:7474
    ```

    Import the Neo4j graph data in a new Command Prompt, using your own neo4j password

    ```powershell
    & "C:\Users\appDB\Documents\neo4j-community-5.26.19\bin\cypher-shell.bat" -u neo4j -p YOUR_NEO4J_PASSWORD -d neo4j -f "C:\Users\appDB\Desktop\Applied Databases Project\appdbprojNeo4j.json"
    ```

   To verify the graph was imported correctly, open Neo4j Browser and run - The following query is run inside Neo4j Browser:

    ```cypher
    MATCH (a:Attendee)-[:CONNECTED_TO]-(b:Attendee)
    RETURN a, b;
    ```

8. Open the project folder and run the application

    ```bash
    python main.py
    ```
    The conference management Menu should now appear  

    ```bash
    Conference Management
    ---------------------

    MENU
    ====
    1 - View Speakers & Sessions
    2 - View Attendees by Company
    3 - Add New Attendee
    4 - View Connected Attendees
    5 - Add Attendee Connection
    6 - View Rooms
    x - Exit application
    Choice:
    ```


## Troubleshooting and Debugging Notes

If connection issues occur, ensure:
- MySQL80 service is running
- Neo4j server is active
- Database credentials in db_connect.py and in Neo4j graph data Import are correct
- Required Python packages are installed

## Innovation

The innovation and technical improvement details for this project are documented separately in innovation.doc
## Contact  
<br/>

Maroua El imame   
Author and sole contributor   
G00472980@atu.ie   
