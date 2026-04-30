# Conference Management Application

## Introduction  

This project is a Python-based terminal application developed as part of the Applied Databases module.  
It allows users to interact with a conference management system using a menu-driven interface.  

The application connects to a MySQL database `appdbproj` to retrieve and manage conference data such as speakers, sessions, attendees, and rooms. It also uses Neo4j to handle relationships between attendees.  

The goal of this project is to design and implement a database-driven application that integrates both relational and graph data models.  


## Environment setup

Install required Python packages:  
--  pip install -r requirements.txt  

Set up the database:  
--  Use the file appdbproj.sql to create the database and tables.  

Set up Neo4j:   
--  Run the queries from appdbprojNeo4j.json  

**!** Note:  
Neo4j is used to store connections between attendees.  
These connections are undirected (if A is connected to B, then B is also connected to A).  
All attendees in Neo4j already exist in the MySQL database.  

**!** Update the MySQL password in db_connect.py before running the application.

Run the Application:  
--  python main.py  

## Project Workflow

The following workflow outlines the step-by-step process of this application based on a structured development approach.  
Each step was implemented progressively, with functionality added and tested throughout the project:

* [✔️] **Repository Setup**  
  Create the project repository and initial file structure.  

* [✔️] **Database Setup**  
  Use the provided `appdbproj.sql` file to set up the database and tables.

* [✔️] **Database Connection**  
  Connect the Python application to the database.

* [✔️] **Menu Implementation**  
  Create a simple menu to allow the user to select different options.  

- [ ] Core Features Development
- [ ] Neo4j Integration  
- [ ] Testing  
- [ ] Finalisation  