from fastapi import FastAPI, HTTPException
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from requests.exceptions import ConnectionError 
from urllib3.exceptions import MaxRetryError
from pydantic import BaseModel, Field
import sqlite3

app = FastAPI()

# ACCEPTABLE ORIGINS
origins = ["http://localhost:5173", "http://127.0.0.1:5173"] 
# CORS_MIDDLEWARE TO PREVENT CORS ISSUE
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

#Pydantic Models
class Task(BaseModel):
    due_date: str
    task: str
    
class TaskGrabber(BaseModel):
    id: int
    due_date: str
    task: str

class TaskPatcher(BaseModel):
    due_date: str | None = None
    task: str | None = None 


# CREATE TASK
@app.post("/create-task", response_model=Task)
def create_tasks(task: Task):
    #Make Databse Connection 
    with sqlite3.connect("tasks.db") as conn:
        cursor = conn.cursor()
        #Insert Task 
        cursor.execute("INSERT INTO Tasks(due_date, task) Values(?, ?)", 
                        (task.due_date, task.task))
    return task
    
# READ TASK
@app.get("/read-task/{id}", response_model=TaskGrabber)
def get_tasks(id: int):
    #Make Databse Connection 
    with sqlite3.connect("tasks.db") as conn:
        cursor = conn.cursor()
        #Insert Task 
        cursor.execute("SELECT * FROM Tasks WHERE id = ?", (id,))
        row = cursor.fetchone()
        if row:
            return {"id": row[0], "due_date": row[1], "task": row[2]}
        else:
            raise HTTPException(status_code=404, detail="Task Not Found")           

# UPDATE TASK
@app.patch("/patch-task/{id}", response_model=TaskPatcher)
def patch_tasks():
    pass

@app.put("/put-task/{id}", response_model=Task)
def put_tasks(id: int, task: Task):
     with sqlite3.connect("tasks.db") as conn:
        cursor = conn.cursor()
        #Update Task
        cursor.execute("UPDATE Tasks SET due_date = ?, task = ? WHERE id = ?", 
                        (task.due_date, task.task, id))
        if not cursor.rowcount:
            raise HTTPException(status_code=404, detail="Task Not Found")           

# DELETE TASK
@app.delete("/delete-task/{id}", response_model=TaskGrabber)
def delete_tasks():
     with sqlite3.connect("tasks.db") as conn:
        cursor = conn.cursor()
        #Update Task
        cursor.execute("DELETE FROM Tasks where id = ?", (id))
        if not cursor.rowcount:
            raise HTTPException(status_code=404, detail="Task Not Found")