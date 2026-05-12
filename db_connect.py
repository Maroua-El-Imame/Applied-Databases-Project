import mysql.connector
from neo4j import GraphDatabase

# MySQL connection 
def get_mysql_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="YOUR_MYSQL_PASSWORD",
        database="appdbproj",
        use_pure=True
    )

# Neo4j connection
def get_neo4j_driver():
    return GraphDatabase.driver(
        "bolt://localhost:7687",
        auth=("neo4j", "YOUR_NEO4J_PASSWORD")
    )
