from fastapi.testclient import TestClient
from api import app
from api import init_db
from test_blackbox import check_existing_table
import sqlite3

#API Section 
client = TestClient(app)

def test_white_box_post():
    #ENDPOINT EXECUTION SUCCESS
    check_existing_table(True)
    task = {"due_date": "2020-02-02", "task": "A"}
    response = client.post("/tasks",json=task)
    assert response.status_code == 201
    assert response.json() == {"id": 1, "due_date": "2020-02-02", "task": "A"}
    
def test_white_box_get():
    check_existing_table(True)
    #ROW EXISTS TRUE BRANCH
    #ROW DOES NOT EXIST BRANCH 
    #ENDPOINT EXECUTION SUCCESS
    task = {"due_date": "2020-02-02", "task": "A"}
    response = client.post("/tasks",json=task)
    response = client.get("/tasks/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "due_date": "2020-02-02", "task": "A"}
    
def test_white_box_patch():
    check_existing_table(True)
    #DYNAMIC QUERY CREATION FOR TASK ONLY
    #DYANMIC QUERY CREATION FOR DUE DATE ONLY
    #DYANMIC QUERY CREATION FOR BOTH 
    #ROW EXISTS TRUE BRANCH
    #ROW DOES NOT EXIST BRANCH 

    #ENDPOINT EXECUTION SUCCESS
    task = {"due_date": "2020-02-02", "task": "A"}
    response = client.post("/tasks",json=task)
    task = {"task": "Abe"}
    response = client.patch("/tasks/1",json=task)
    assert response.status_code == 200
    assert response.json() == {"id": 1, "due_date": "2020-02-02", "task": "Abe"}
    
def test_white_box_put():
    check_existing_table(True)
    #ROW EXISTS TRUE BRANCH
    #ROW DOES NOT EXIST BRANCH 

    #ENDPOINT EXECUTION SUCCESS
    task = {"due_date": "2020-02-02", "task": "A"}
    response = client.post("/tasks",json=task)
    task = {"due_date": "2020-02-04", "task": "Abe"}
    response = client.put("/tasks/1",json=task)
    assert response.status_code == 200
    assert response.json() == {"id": 1, "due_date": "2020-02-04", "task": "Abe"}
    pass
def test_white_box_delete():
    check_existing_table(True)
    #ROW EXISTS TRUE BRANCH
    #ROW DOES NOT EXIST BRANCH 
    #ENDPOINT EXECUTION SUCCESS
    task = {"due_date": "2020-02-02", "task": "A"}
    response = client.post("/tasks",json=task)
    response = client.delete("/tasks/1")
    assert response.status_code == 204
