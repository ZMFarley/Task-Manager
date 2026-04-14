from fastapi.testclient import TestClient
from api import app
from api import init_db
import sqlite3

#API Section 
client = TestClient(app)

#Test Setup

#Delete any currently active tables to allow for fresh testing 
with sqlite3.connect("tasks.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS TASKS")

#Reinitalize table for testing
init_db()

#White Box Tests

#Black Box Tests

#Test Completion
#Drop test table
with sqlite3.connect("tasks.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS TASKS")
