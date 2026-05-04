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

- [Processing] **Neo4j Feature Preparation**  
  Added the Neo4j driver connection and prepared the project structure for graph-based attendee connection features.

- [Processing] **Testing**  
  Tested implemented options, database connections, menu flow, and VM compatibility.

- [ ] **Finalisation**  
  Complete remaining Neo4j features, final testing, documentation, and submission preparation.

 


## Environment Setup & App Running

1. Download and unzip the project folder.

2.  Open Command Prompt or PowerShell in the project folder.

    Example:
    ```bash
    cd Downloads/Applied-Databases-Project  
    ```
   
3. Install required Python packages:  
   ```bash
    pip install -r requirements.txt
    ```

4. Ensure MySQL Server is running.
   ```bash
   net start MySQL80

5. Update database credentials in "db_connect.py".

   Update the MySQL and Neo4j username/password values so they match the local machine or VM.

   Example:
   ```bash
   MySQL - 
   password="YOUR_MYSQL_PASSWORD"
   Neo4j -
   auth=("neo4j", "YOUR_NEO4J_PASSWORD")

6. Set up the MySQL database  

    ```bash
    ```

7. Set up Neo4j  
    ```bash
    ```

8. Run the application

    ```bash
    python main.py
    ```

    ```bash
    ```


## Troubleshooting and Debugging Notes

## Innovation

The innovation and technical improvement details for this project are documented separately in `innovation.doc`  


## Contact  
<br/>

Maroua El imame   
Author and sole contributor   
G00472980@atu.ie   
