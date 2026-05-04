import mysql.connector
from neo4j import GraphDatabase

# MySQL connection 
def get_mysql_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="sql1225**",
        database="appdbproj"
    )

# Neo4j connection
def get_neo4j_driver():
    return GraphDatabase.driver(
        "bolt://localhost:7687",
        auth=("neo4j", "neo4jneo4j")
    )
