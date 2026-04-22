from fastapi.testclient import TestClient
from api import app
from test_blackbox import check_existing_table

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
    #ENDPOINT EXECUTION SUCCESS/#ROW EXISTS TRUE BRANCH
    task = {"due_date": "2020-02-02", "task": "A"}
    response = client.post("/tasks",json=task)
    response = client.get("/tasks/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "due_date": "2020-02-02", "task": "A"}
    
    #ROW DOES NOT EXIST BRANCH 
    response = client.get("/tasks/2")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Task Not Found'}

def test_white_box_patch():
    check_existing_table(True)
    #TEST SETUP
    task = {"due_date": "2020-02-02", "task": "A"}
    response = client.post("/tasks",json=task)

    #DYNAMIC QUERY CREATION FOR TASK ONLY/ENDPOINT SUCCESS/ROW EXISTS TRUE BRANCH
    task = {"task": "Abe"}
    response = client.patch("/tasks/1",json=task)
    assert response.status_code == 200
    assert response.json() == {"id": 1, "due_date": "2020-02-02", "task": "Abe"}

    #DYANMIC QUERY CREATION FOR DUE DATE ONLY/ENDPOINT SUCCESS/ROW EXISTS TRUE BRANCH
    task = {"due_date": "1820-12-31"}
    response = client.patch("/tasks/1",json=task)
    assert response.status_code == 200
    assert response.json() == {"id": 1, "due_date": "1820-12-31", "task": "Abe"}

    #DYANMIC QUERY CREATION FOR BOTH/ENDPOINT SUCCESS/ROW EXISTS TRUE BRANCH
    task = {"due_date": "1911-03-23","task": "Abel"}
    response = client.patch("/tasks/1",json=task)
    assert response.status_code == 200
    assert response.json() == {"id": 1, "due_date": "1911-03-23","task": "Abel"}
   
    #ROW DOES NOT EXIST BRANCH 
    task = {"due_date": "1911-03-21","task": "Abela"}
    response = client.patch("/tasks/2",json=task)
    assert response.status_code == 404
    assert response.json() == {'detail': 'Task Not Found'}

    #NO TASKS HAVE BEEN PASSED 
    response = client.patch("/tasks/1", json={})
    assert response.status_code == 400
    assert response.json() == {'detail': 'No Data provided'}

def test_white_box_put():
    #TASK SET UP 
    check_existing_table(True)
    task = {"due_date": "2020-02-02", "task": "A"}
    response = client.post("/tasks",json=task)

    #ROW EXISTS TRUE BRANCH/ENDPOINT EXECUTION SUCCESS
    task = {"due_date": "2020-02-04", "task": "Abe"}
    response = client.put("/tasks/1",json=task)
    assert response.status_code == 200
    assert response.json() == {"id": 1, "due_date": "2020-02-04", "task": "Abe"}

    #ROW DOES NOT EXIST BRANCH 
    task = {"due_date": "1911-03-21","task": "Abela"}
    response = client.put("/tasks/2",json=task)
    assert response.status_code == 404
    assert response.json() == {'detail': 'Task Not Found'}

def test_white_box_delete():
    check_existing_table(True)

    #ROW EXISTS TRUE BRANCH/ENDPOINT EXECUTION SUCCESS
    task = {"due_date": "2020-02-02", "task": "A"}
    response = client.post("/tasks",json=task)
    response = client.delete("/tasks/1")
    assert response.status_code == 204

    #ROW DOES NOT EXIST BRANCH 
    response = client.delete("/tasks/2")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Task Not Found'}