from fastapi.testclient import TestClient
from api import app
from api import init_db
import sqlite3

#API Section 
client = TestClient(app)

def check_existing_table(flag: bool):
        #Test Setup

        #Delete any currently active tables to allow for fresh testing 
        with sqlite3.connect("tasks.db") as conn:
                cursor = conn.cursor()
                cursor.execute("DROP TABLE IF EXISTS TASKS")

        #Reinitalize table for testing if being used to start up testing
        if flag:
                init_db()
def test_black_box_post():
        #Test Setup
        check_existing_table(True)
        #Black Box Tests for POST requests
        #BVA AND ECP TEST CASES FOR TASK INPUT

        '''
           BVA/ECP TESTING FOR TASK FIELD
        '''
        #BVA/ECP MIN- LENGTH STRING TASK (Empty String)
        task = {"due_date": "2020-02-02", "task": ""}
        response = client.post("/tasks",json=task)
        assert response.status_code == 422
        assert response.json()["detail"][0]['msg'] == 'String should have at least 1 character'

        #BVA MIN Length (1) STRING TASK
        task = {"due_date": "2020-02-02", "task": "A"}
        response = client.post("/tasks",json=task)
        assert response.status_code == 201
        assert response.json() == {"id": 1, "due_date": "2020-02-02", "task": "A"}

        #BVA/ECP  (MIN+) MIDDLE LENGTH STRING TASK
        task = {"due_date": "2024-04-02", "task": "PA"}
        response = client.post("/tasks",json=task)
        assert response.status_code == 201
        assert response.json() == {"id": 2, "due_date": "2024-04-02", "task": "PA"}

        #BVA MAX- LENGTH STRING 254 CHARACTERS
        task = {"due_date": "1923-12-01", "task": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}
        response = client.post("/tasks",json=task)
        assert response.status_code == 201
        assert response.json() == {"id": 3, "due_date": "1923-12-01", "task": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}
        
        #BVA MAX LENGTH STRING 255 CHARACTERS
        task = {"due_date": "1999-12-01", "task": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}
        response = client.post("/tasks",json=task)
        assert response.status_code == 201
        assert response.json() == {"id": 4, "due_date": "1999-12-01", "task": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}
        
        #ECP MAX+ LENGTH STRING TASK 256 CHARACTERS
        task = {"due_date": "2020-02-02", "task": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}
        response = client.post("/tasks",json=task)
        assert response.status_code == 422
        assert response.json()["detail"][0]['msg'] == 'String should have at most 255 characters'

        #ECP MISSING TASKS
        task = {"due_date": "2020-02-02"}
        response = client.post("/tasks",json=task)
        assert response.status_code == 422
        assert response.json()["detail"][0]['msg'] == 'Field required'

        #ECP NULL VALUE FOR TASK
        task = {"due_date": "2020-02-02", "task": None}
        response = client.post("/tasks",json=task)
        assert response.status_code == 422

        '''
        BVA/ECP TESTING FOR DUE DATE FIELD
        '''
        #BVA/ECP MIN- DATE 
        task = {"due_date": "0000-01-01", "task": "fly to the moon"}
        response = client.post("/tasks",json=task)
        assert response.status_code == 422
        assert response.json()["detail"][0]['msg'] == 'Input should be a valid date in the format YYYY-MM-DD, year 0 is out of range'

        #BVA/ECP MIN DATE (0001-01-01)
        task = {"due_date": "0001-01-01", "task": "itch my foot"}
        response = client.post("/tasks",json=task)
        assert response.status_code == 201
        assert response.json() == {"id": 5, "due_date": "0001-01-01", "task": "itch my foot"}

        #BVA/ECP MIN+ DATE (0002-01-01)
        task = {"due_date": "0002-01-01", "task": "itch my leg"}
        response = client.post("/tasks",json=task)
        assert response.status_code == 201
        assert response.json() == {"id": 6, "due_date": "0002-01-01", "task": "itch my leg"}
        
        #ECP INCORRECT FORMAT MM/DD/YYYY OR DD/MM/YYYY, BOTH WILL BE TREATED THE SAME
        task = {"due_date": "04/20/1920", "task": "fly to the clouds"}
        response = client.post("/tasks",json=task)
        assert response.status_code == 422
        assert response.json()["detail"][0]['msg'] == 'Input should be a valid date or datetime, invalid character in year'

        #ECP INCORRECT FORMAT MM-DD-YYYY OR DD-MM-YYYY, BOTH WILL BE TREATED THE SAME
        task = {"due_date": "09-12-1920", "task": "fly to the sky"}
        response = client.post("/tasks",json=task)
        assert response.status_code == 422
        assert response.json()["detail"][0]['msg'] == 'Input should be a valid date or datetime, invalid character in year'

        #ECP INVALID DATE, NON EXISTENT DATE 
        task = {"due_date": "02-30-1920", "task": "fly to the Barber"}
        response = client.post("/tasks",json=task)
        assert response.status_code == 422
        assert response.json()["detail"][0]['msg'] == 'Input should be a valid date or datetime, invalid character in year'

        #BVA MAX DATE (9999-12-31)
        task = {"due_date": "9999-12-31", "task": "take out the trash"}
        response = client.post("/tasks",json=task)
        assert response.status_code == 201
        assert response.json() == {"id": 7, "due_date": "9999-12-31", "task": "take out the trash"}
        
        #BVA/ECP MAX+ DATE 
        task = {"due_date": "10000-12-31", "task": "take out the trash"}
        response = client.post("/tasks",json=task)
        assert response.status_code == 422
        assert response.json()["detail"][0]['msg'] == 'Input should be a valid date or datetime, invalid date separator, expected `-`'
        
        #ECP MISSING DUE DATE
        task = {"task": "run"}
        response = client.post("/tasks",json=task)
        assert response.status_code == 422
        assert response.json()["detail"][0]['msg'] == 'Field required'

        #ECP NULL VALUE FOR DUE DATE
        task = {"due_date": None, "task": "bob"}
        response = client.post("/tasks",json=task)
        assert response.status_code == 422

        #Test Completion
        #Drop test table
        check_existing_table(False)

def test_black_box_get():
        #Task set up for testing
        check_existing_table(True)
        client.post("/tasks",json={"due_date": "1220-12-31", "task": "Do whatever the Romans do"})
        client.post("/tasks",json={"due_date": "1492-12-31", "task": "Sail the Ocean Blue"})

        '''
        BVA/ECP TESTING FOR ID FIELD
        '''

        #BVA/ECP MIN- ID (0)
        response = client.get("/tasks/0")
        assert response.status_code == 422
        assert response.json()["detail"][0]['msg'] == 'Input should be greater than 0'

        #BVA/ECP MIN ID (1)
        response = client.get("/tasks/1")
        assert response.status_code == 200
        assert response.json() == {"id": 1, "due_date": "1220-12-31", "task": "Do whatever the Romans do"}

        #BVA/ECP MIN+ ID
        response = client.get("/tasks/2")
        assert response.status_code == 200
        assert response.json() == {"id": 2, "due_date": "1492-12-31", "task": "Sail the Ocean Blue"}


        #BVA/ECP MAX- (9223372036854775806)
        with sqlite3.connect("tasks.db") as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO Tasks(id, due_date, task) VALUES (?, ?, ?)",
                (9223372036854775806, "2024-01-23", "Run"))
        response = client.get("/tasks/9223372036854775806")
        assert response.status_code == 200
        assert response.json() == {"id": 9223372036854775806, "due_date": "2024-01-23", "task": "Run"}

        #BVA/ECP MAX (9223372036854775807)
        with sqlite3.connect("tasks.db") as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO Tasks(id, due_date, task) VALUES (?, ?, ?)",
                (9223372036854775807, "2025-01-24", "Run Faster"))
        response = client.get("/tasks/9223372036854775807")
        assert response.status_code == 200
        assert response.json() == {"id": 9223372036854775807, "due_date": "2025-01-24", "task": "Run Faster"}
        
        #BVA/ECP MAX+ (9223372036854775808)
        response = client.get("/tasks/9223372036854775808")
        assert response.status_code == 422
        assert response.json()["detail"][0]['msg'] == 'Input should be less than or equal to 9223372036854775807'

        #ECP NON EXISTING VALID ID
        response = client.get("/tasks/3")
        assert response.status_code == 404
        assert response.json()["detail"] == 'Task Not Found'

        #ECP NON NUMERIC INPUT
        response = client.get("/tasks/abc")
        assert response.status_code == 422
        assert response.json()["detail"][0]['msg'] == 'Input should be a valid integer, unable to parse string as an integer'

        #ECP INVALID FLOAT INPUT
        response = client.get("/tasks/1.5")
        assert response.status_code == 422
        assert response.json()["detail"][0]['msg'] == 'Input should be a valid integer, unable to parse string as an integer'

        check_existing_table(False)

def test_black_box_patch():
        '''
        BVA/ECP TESTING FOR ID FIELD
        '''
        #Task set up for testing
        check_existing_table(True)
        client.post("/tasks",json={"due_date": "1220-12-31", "task": "Do whatever the Romans do"})
        client.post("/tasks",json={"due_date": "1492-12-31", "task": "Sail the Ocean Blue"})

        task = {"due_date": "1220-12-31", "task": "A"}
        #BVA/ECP MIN- ID (0)
        response = client.patch("/tasks/0", json=task)
        assert response.status_code == 422
        assert response.json()["detail"][0]['msg'] == 'Input should be greater than 0'

        #BVA/ECP MIN ID (1)
        response = client.patch("/tasks/1", json=task)
        assert response.status_code == 200

        #BVA/ECP MIN+ ID
        response = client.patch("/tasks/2", json=task)
        assert response.status_code == 200

        #BVA/ECP MAX- (9223372036854775806)
        with sqlite3.connect("tasks.db") as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO Tasks(id, due_date, task) VALUES (?, ?, ?)",
                (9223372036854775806, "2024-01-23", "Run"))
        response = client.patch("/tasks/9223372036854775806",json=task)
        assert response.status_code == 200

        #BVA/ECP MAX (9223372036854775807)
        with sqlite3.connect("tasks.db") as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO Tasks(id, due_date, task) VALUES (?, ?, ?)",
                (9223372036854775807, "2025-01-24", "Run Faster"))
        response = client.patch("/tasks/9223372036854775807", json=task)
        assert response.status_code == 200
        
        #BVA/ECP MAX+ (9223372036854775808)
        response = client.patch("/tasks/9223372036854775808", json=task)
        assert response.status_code == 422
        assert response.json()["detail"][0]['msg'] == 'Input should be less than or equal to 9223372036854775807'

        #ECP NON EXISTING VALID ID
        response = client.patch("/tasks/3", json=task)
        assert response.status_code == 404
        assert response.json()["detail"] == 'Task Not Found'

        #ECP NON NUMERIC INPUT
        response = client.patch("/tasks/abc", json=task)
        assert response.status_code == 422
        assert response.json()["detail"][0]['msg'] == 'Input should be a valid integer, unable to parse string as an integer'

        #ECP INVALID FLOAT INPUT
        response = client.patch("/tasks/1.5", json=task)
        assert response.status_code == 422
        assert response.json()["detail"][0]['msg'] == 'Input should be a valid integer, unable to parse string as an integer'

        '''
        BVA/ECP TESTING FOR TASK FIELD
        '''
        check_existing_table(True)
        client.post("/tasks",json={"due_date": "1220-12-31", "task": "Do whatever the Romans do"})

        #BVA/ECP MIN- LENGTH STRING TASK (Empty String)
        task = {"task": ""}
        response = client.patch("/tasks/1",json=task)
        assert response.status_code == 422
        assert response.json()["detail"][0]['msg'] == 'String should have at least 1 character'

        #BVA MIN Length (1) STRING TASK
        task = {"task": "A"}
        response = client.patch("/tasks/1",json=task)
        assert response.status_code == 200
        assert response.json() == {"id": 1, "due_date": "1220-12-31", "task": "A"}

        #BVA/ECP  (MIN+) MIDDLE LENGTH STRING TASK
        task = {"task": "PA"}
        response = client.patch("/tasks/1",json=task)
        assert response.status_code == 200
        assert response.json() == {"id": 1, "due_date": "1220-12-31", "task": "PA"}

        #BVA MAX- LENGTH STRING 254 CHARACTERS
        task = {"task": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}
        response = client.patch("/tasks/1",json=task)
        assert response.status_code == 200
        assert response.json() == {"id": 1, "due_date": "1220-12-31", "task": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}
        
        #BVA MAX LENGTH STRING 255 CHARACTERS
        task = {"task": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}
        response = client.patch("/tasks/1",json=task)
        assert response.status_code == 200
        assert response.json() == {"id": 1, "due_date": "1220-12-31", "task": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}
        
        #ECP MAX+ LENGTH STRING TASK 256 CHARACTERS
        task = {"task": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}
        response = client.patch("/tasks/1",json=task)
        assert response.status_code == 422
        assert response.json()["detail"][0]['msg'] == 'String should have at most 255 characters'

        #ECP NULL VALUE FOR TASK
        task = {"task": None}
        response = client.patch("/tasks/1",json=task)
        assert response.status_code == 422

        '''
        BVA/ECP TESTING FOR DUE DATE FIELD
        '''
        check_existing_table(True)
        client.post("/tasks",json={"due_date": "1220-12-31", "task": "Do whatever the Romans do"})

        #BVA/ECP MIN- DATE 
        task = {"due_date": "0000-01-01"}
        response = client.patch("/tasks/1",json=task)
        assert response.status_code == 422
        assert response.json()["detail"][0]['msg'] == 'Input should be a valid date in the format YYYY-MM-DD, year 0 is out of range'

        #BVA/ECP MIN DATE (0001-01-01)
        task = {"due_date": "0001-01-01"}
        response = client.patch("/tasks/1",json=task)
        assert response.status_code == 200
        assert response.json() == {"id": 1, "due_date": "0001-01-01", "task": "Do whatever the Romans do"}

        #BVA/ECP MIN+ DATE (0002-01-01)
        task = {"due_date": "0002-01-01"}
        response = client.patch("/tasks/1",json=task)
        assert response.status_code == 200
        assert response.json() == {"id": 1, "due_date": "0002-01-01", "task": "Do whatever the Romans do"}
        
        #ECP INCORRECT FORMAT MM/DD/YYYY OR DD/MM/YYYY, BOTH WILL BE TREATED THE SAME
        task = {"due_date": "04/20/1920"}
        response = client.patch("/tasks/1",json=task)
        assert response.status_code == 422
        assert response.json()["detail"][0]['msg'] == 'Input should be a valid date or datetime, invalid character in year'

        #ECP INCORRECT FORMAT MM-DD-YYYY OR DD-MM-YYYY, BOTH WILL BE TREATED THE SAME
        task = {"due_date": "09-12-1920"}
        response = client.patch("/tasks/1",json=task)
        assert response.status_code == 422
        assert response.json()["detail"][0]['msg'] == 'Input should be a valid date or datetime, invalid character in year'

        #ECP INVALID DATE, NON EXISTENT DATE 
        task = {"due_date": "02-30-1920"}
        response = client.patch("/tasks/1",json=task)
        assert response.status_code == 422
        assert response.json()["detail"][0]['msg'] == 'Input should be a valid date or datetime, invalid character in year'

        #BVA MAX DATE (9999-12-31)
        task = {"due_date": "9999-12-31"}
        response = client.patch("/tasks/1",json=task)
        assert response.status_code == 200
        assert response.json() == {"id": 1, "due_date": "9999-12-31", "task": "Do whatever the Romans do"}
        
        #BVA/ECP MAX+ DATE 
        task = {"due_date": "10000-12-31"}
        response = client.patch("/tasks/1",json=task)
        assert response.status_code == 422
        assert response.json()["detail"][0]['msg'] == 'Input should be a valid date or datetime, invalid date separator, expected `-`'

        #ECP NULL VALUE FOR TASK
        task = {"due_date": None}
        response = client.patch("/tasks/1",json=task)
        assert response.status_code == 422
        #Test Completion

        '''
        BVA/ECP TESTING FOR BOTH FIELDS
        '''
        check_existing_table(True)
        client.post("/tasks",json={"due_date": "1220-12-31", "task": "Do whatever the Romans do"})

        #ECP to change both fields with valid payload
        task = {"due_date": "1220-12-30", "task": "A"}
        response = client.patch("/tasks/1", json=task)
        assert response.status_code == 200
        assert response.json() == {"id": 1, "due_date": "1220-12-30", "task": "A"}

        #ECP Invalid due date with valid task
        task = {"due_date": "1220/12/31", "task": "A"}
        response = client.patch("/tasks/1", json=task)
        assert response.status_code == 422
        assert response.json()["detail"][0]['msg'] == "Input should be a valid date or datetime, invalid date separator, expected `-`"
        
        #ECP Valid due date with invalid task
        task = {"due_date": "1220-12-31", "task": ""}
        response = client.patch("/tasks/1", json=task)
        assert response.status_code == 422
        assert response.json()["detail"][0]['msg'] == 'String should have at least 1 character'
        
        #ECP both invalid fields
        task = {"due_date": "1220/12/31", "task": ""}
        response = client.patch("/tasks/1", json=task)
        assert response.status_code == 422
        
        #ECP Empty task and due date
        task = {}
        response = client.patch("/tasks/1", json=task)
        assert response.status_code == 400
        assert response.json()["detail"] == "No Data provided"

        #ECP NONE IN BOTH FIELDS
        task = {"due_date": None, "task": None}
        response = client.patch("/tasks/1", json=task)
        assert response.status_code == 422

        #Clear the Database
        check_existing_table(False)

def test_black_box_put():
        
        '''
        BVA/ECP TESTING FOR ID FIELD
        '''
        #Task set up for testing
        check_existing_table(True)
        client.post("/tasks",json={"due_date": "1220-12-31", "task": "Do whatever the Romans do"})
        client.post("/tasks",json={"due_date": "1492-12-31", "task": "Sail the Ocean Blue"})

        task = {"due_date": "1220-12-31", "task": "A"}
        #BVA/ECP MIN- ID (0)
        response = client.put("/tasks/0", json=task)
        assert response.status_code == 422
        assert response.json()["detail"][0]['msg'] == 'Input should be greater than 0'

        #BVA/ECP MIN ID (1)
        response = client.put("/tasks/1", json=task)
        assert response.status_code == 200

        #BVA/ECP MIN+ ID
        response = client.put("/tasks/2", json=task)
        assert response.status_code == 200

        #BVA/ECP MAX- (9223372036854775806)
        with sqlite3.connect("tasks.db") as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO Tasks(id, due_date, task) VALUES (?, ?, ?)",
                (9223372036854775806, "2024-01-23", "Run"))
        response = client.put("/tasks/9223372036854775806",json=task)
        assert response.status_code == 200

        #BVA/ECP MAX (9223372036854775807)
        with sqlite3.connect("tasks.db") as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO Tasks(id, due_date, task) VALUES (?, ?, ?)",
                (9223372036854775807, "2025-01-24", "Run Faster"))
        response = client.put("/tasks/9223372036854775807", json=task)
        assert response.status_code == 200
        
        #BVA/ECP MAX+ (9223372036854775808)
        response = client.put("/tasks/9223372036854775808", json=task)
        assert response.status_code == 422
        assert response.json()["detail"][0]['msg'] == 'Input should be less than or equal to 9223372036854775807'

        #ECP NON EXISTING VALID ID
        response = client.put("/tasks/3", json=task)
        assert response.status_code == 404
        assert response.json()["detail"] == 'Task Not Found'

        #ECP NON NUMERIC INPUT
        response = client.put("/tasks/abc", json=task)
        assert response.status_code == 422
        assert response.json()["detail"][0]['msg'] == 'Input should be a valid integer, unable to parse string as an integer'

        #ECP INVALID FLOAT INPUT
        response = client.put("/tasks/1.5", json=task)
        assert response.status_code == 422
        assert response.json()["detail"][0]['msg'] == 'Input should be a valid integer, unable to parse string as an integer'

        '''
        BVA/ECP TESTING FOR TASK FIELD
        '''
        check_existing_table(True)
        client.post("/tasks",json={"due_date": "1220-12-31", "task": "Do whatever the Romans do"})
        #BVA/ECP MIN- LENGTH STRING TASK (Empty String)
        task = {"due_date": "1220-12-31", "task": ""}
        response = client.put("/tasks/1",json=task)
        assert response.status_code == 422
        assert response.json()["detail"][0]['msg'] == 'String should have at least 1 character'

        #BVA MIN Length (1) STRING TASK
        task = {"due_date": "1220-12-31", "task": "A"}
        response = client.put("/tasks/1",json=task)
        assert response.status_code == 200
        assert response.json() == {"id": 1, "due_date": "1220-12-31", "task": "A"}

        #BVA/ECP  (MIN+) MIDDLE LENGTH STRING TASK
        task = {"due_date": "1220-12-31", "task": "PA"}
        response = client.put("/tasks/1",json=task)
        assert response.status_code == 200
        assert response.json() == {"id": 1, "due_date": "1220-12-31", "task": "PA"}

        #BVA MAX- LENGTH STRING 254 CHARACTERS
        task = {"due_date": "1220-12-31", "task": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}
        response = client.put("/tasks/1",json=task)
        assert response.status_code == 200
        assert response.json() == {"id": 1, "due_date": "1220-12-31", "task": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}
        
        #BVA MAX LENGTH STRING 255 CHARACTERS
        task = {"due_date": "1220-12-31", "task": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}
        response = client.put("/tasks/1",json=task)
        assert response.status_code == 200
        assert response.json() == {"id": 1, "due_date": "1220-12-31", "task": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}
        
        #ECP MAX+ LENGTH STRING TASK 256 CHARACTERS
        task = {"due_date": "1220-12-31", "task": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}
        response = client.put("/tasks/1",json=task)
        assert response.status_code == 422
        assert response.json()["detail"][0]['msg'] == 'String should have at most 255 characters'

        #ECP MISSING task
        task = {"due_date": "1220-12-31"}
        response = client.put("/tasks/1",json=task)
        assert response.status_code == 422
        assert response.json()["detail"][0]['msg'] == 'Field required'
        
        '''
        BVA/ECP TESTING FOR DUE DATE FIELD
        '''
        #BVA/ECP MIN- DATE 
        task = {"due_date": "0000-01-01", "task": "fly to the moon"}
        response = client.put("/tasks/1",json=task)
        assert response.status_code == 422
        assert response.json()["detail"][0]['msg'] == 'Input should be a valid date in the format YYYY-MM-DD, year 0 is out of range'

        #BVA/ECP MIN DATE (0001-01-01)
        task = {"due_date": "0001-01-01", "task": "fly to the moon"}
        response = client.put("/tasks/1",json=task)
        assert response.status_code == 200
        assert response.json() == {"id": 1, "due_date": "0001-01-01", "task": "fly to the moon"}

        #BVA/ECP MIN+ DATE (0002-01-01)
        task = {"due_date": "0002-01-01", "task": "fly to the moon"}
        response = client.put("/tasks/1",json=task)
        assert response.status_code == 200
        assert response.json() == {"id": 1, "due_date": "0002-01-01", "task": "fly to the moon"}
        
        #ECP INCORRECT FORMAT MM/DD/YYYY OR DD/MM/YYYY, BOTH WILL BE TREATED THE SAME
        task = {"due_date": "04/20/1920", "task": "fly to the moon"}
        response = client.put("/tasks/1",json=task)
        assert response.status_code == 422
        assert response.json()["detail"][0]['msg'] == 'Input should be a valid date or datetime, invalid character in year'

        #ECP INCORRECT FORMAT MM-DD-YYYY OR DD-MM-YYYY, BOTH WILL BE TREATED THE SAME
        task = {"due_date": "09-12-1920", "task": "fly to the moon"}
        response = client.put("/tasks/1",json=task)
        assert response.status_code == 422
        assert response.json()["detail"][0]['msg'] == 'Input should be a valid date or datetime, invalid character in year'

        #ECP INVALID DATE, NON EXISTENT DATE 
        task = {"due_date": "02-30-1920", "task": "fly to the moon"}
        response = client.put("/tasks/1",json=task)
        assert response.status_code == 422
        assert response.json()["detail"][0]['msg'] == 'Input should be a valid date or datetime, invalid character in year'

        #BVA MAX DATE (9999-12-31)
        task = {"due_date": "9999-12-31", "task": "fly to the moon"}
        response = client.put("/tasks/1",json=task)
        assert response.status_code == 200
        assert response.json() == {"id": 1, "due_date": "9999-12-31", "task": "fly to the moon"}
        
        #BVA/ECP MAX+ DATE 
        task = {"due_date": "10000-12-31", "task": "fly to the moon"}
        response = client.put("/tasks/1",json=task)
        assert response.status_code == 422
        assert response.json()["detail"][0]['msg'] == 'Input should be a valid date or datetime, invalid date separator, expected `-`'
        
        #ECP MISSING TASK
        task = {"task": "high five"}
        response = client.put("/tasks/1",json=task)
        assert response.status_code == 422
        assert response.json()["detail"][0]['msg'] == 'Field required'

        #Test Completion
        #Drop test table
        check_existing_table(False)

def test_black_box_delete():
        #Task set up for testing
        check_existing_table(True)
        client.post("/tasks",json={"due_date": "1220-12-31", "task": "Do whatever the Romans do"})
        client.post("/tasks",json={"due_date": "1492-12-31", "task": "Sail the Ocean Blue"})

        '''
        BVA/ECP TESTING FOR ID FIELD
        '''

        #BVA/ECP MIN- ID (0)
        response = client.delete("/tasks/0")
        assert response.status_code == 422
        assert response.json()["detail"][0]['msg'] == 'Input should be greater than 0'

        #BVA/ECP MIN ID (1)
        response = client.delete("/tasks/1")
        assert response.status_code == 204

        #BVA/ECP MIN+ ID
        response = client.delete("/tasks/2")
        assert response.status_code == 204

        #BVA/ECP MAX- (9223372036854775806)
        with sqlite3.connect("tasks.db") as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO Tasks(id, due_date, task) VALUES (?, ?, ?)",
                (9223372036854775806, "2024-01-23", "Run"))
        response = client.delete("/tasks/9223372036854775806")
        assert response.status_code == 204

        #BVA/ECP MAX (9223372036854775807)
        with sqlite3.connect("tasks.db") as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO Tasks(id, due_date, task) VALUES (?, ?, ?)",
                (9223372036854775807, "2025-01-24", "Run Faster"))
        response = client.delete("/tasks/9223372036854775807")
        assert response.status_code == 204
        
        #BVA/ECP MAX+ (9223372036854775808)
        response = client.delete("/tasks/9223372036854775808")
        assert response.status_code == 422
        assert response.json()["detail"][0]['msg'] == 'Input should be less than or equal to 9223372036854775807'

        #ECP NON EXISTING VALID ID
        response = client.delete("/tasks/3")
        assert response.status_code == 404
        assert response.json()["detail"] == 'Task Not Found'

        #ECP NON NUMERIC INPUT
        response = client.delete("/tasks/abc")
        assert response.status_code == 422
        assert response.json()["detail"][0]['msg'] == 'Input should be a valid integer, unable to parse string as an integer'

        #ECP INVALID FLOAT INPUT
        response = client.delete("/tasks/1.5")
        assert response.status_code == 422
        assert response.json()["detail"][0]['msg'] == 'Input should be a valid integer, unable to parse string as an integer'

        #ECP DELETE TWICE 
        client.post("/tasks",json={"due_date": "1492-12-31", "task": "Sail the Ocean Blue"})
        response = client.delete("/tasks/3")
        response = client.delete("/tasks/3")
        assert response.status_code == 404
        assert response.json()["detail"] == 'Task Not Found'
        check_existing_table(False)