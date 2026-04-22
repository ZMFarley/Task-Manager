from fastapi import FastAPI, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import sqlite3
from datetime import date
from contextlib import asynccontextmanager
from typing import Annotated

#Lifespan to create database if it doesnt exist
@asynccontextmanager
async def lifespan (app: FastAPI):
    #Load the Database
    init_db()
    yield

app = FastAPI(lifespan=lifespan)
    
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
    due_date: date
    task: str = Field(min_length=1, max_length=255)
    
class TaskGrabber(BaseModel):
    id: int
    due_date: date
    task: str = Field(min_length=1, max_length=255)

class TaskPatch(BaseModel):
    due_date: date | None = None
    task: str | None = Field(default=None, min_length=1, max_length=255)  


# CREATE TASK
@app.post("/tasks", response_model=TaskGrabber, status_code=201)
def create_tasks(task: Task):
    #Make Database Connection 
    with sqlite3.connect("tasks.db") as conn:
        cursor = conn.cursor()
        #Insert Task 
        cursor.execute("INSERT INTO Tasks(due_date, task) Values(?, ?)", 
                        (task.due_date, task.task))
        #Return Entry
        cursor.execute("SELECT * FROM Tasks WHERE id = ?", (cursor.lastrowid,))
        row = cursor.fetchone()
        return {"id": row[0], "due_date": row[1], "task": row[2]}
    
    
# READ TASK
@app.get("/tasks/{id}", response_model=TaskGrabber)
#
def get_tasks(id: Annotated[int, Path(title="Bounds of ID",gt=0,le=9223372036854775807)]):
    #Make Database Connection 
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
@app.patch("/tasks/{id}", response_model=TaskGrabber)
def patch_tasks(id: Annotated[int, Path(title="Bounds of ID",gt=0,le=9223372036854775807)], task: TaskPatch):
    tasks = task.model_dump(exclude_unset=True)
    query = []
    values = []

    #Create the payload, accounting for optional fields
    if not tasks:
        raise HTTPException(status_code=400, detail="No Data provided")

    for key, value in tasks.items():
        query.append(f"{key} = ?")
        values.append(value)

    with sqlite3.connect("tasks.db") as conn:
        cursor = conn.cursor()
        #Put Task
        cursor.execute(f"UPDATE Tasks SET {', '.join(query)} WHERE id = ?", 
                        (*values, id))
        if not cursor.rowcount:
            raise HTTPException(status_code=404, detail="Task Not Found")
        #Return Entry
        cursor.execute("SELECT * FROM Tasks WHERE id = ?", (id,))
        row = cursor.fetchone()
        return {"id": row[0], "due_date": row[1], "task": row[2]}        

@app.put("/tasks/{id}", response_model=TaskGrabber)
def put_tasks(id: Annotated[int, Path(title="Bounds of ID",gt=0,le=9223372036854775807)], task: Task):
     with sqlite3.connect("tasks.db") as conn:
        cursor = conn.cursor()
        #Put Task
        cursor.execute("UPDATE Tasks SET due_date = ?, task = ? WHERE id = ?", 
                        (task.due_date, task.task, id))
        if not cursor.rowcount:
            raise HTTPException(status_code=404, detail="Task Not Found")
        #Return Entry
        cursor.execute("SELECT * FROM Tasks WHERE id = ?", (id,))
        row = cursor.fetchone()
        return {"id": row[0], "due_date": row[1], "task": row[2]}             

# DELETE TASK
@app.delete("/tasks/{id}", status_code=204)
def delete_tasks(id: Annotated[int, Path(title="Bounds of ID",gt=0,le=9223372036854775807)]):
     with sqlite3.connect("tasks.db") as conn:
        cursor = conn.cursor()
        #Update Task
        cursor.execute("DELETE FROM Tasks where id = ?", (id,))
        if not cursor.rowcount:
            raise HTTPException(status_code=404, detail="Task Not Found")
        
# Helper Function Section
def init_db():
    with sqlite3.connect("tasks.db") as conn:
        cursor = conn.cursor()
        #Read in the schema
        with open("db.sql", "r") as file:
            schema = file.read()
        #Load table
        cursor.execute(schema)