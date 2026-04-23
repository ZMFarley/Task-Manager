# How to Set up and run
- This project in its current format requires simply the installation of the dependencies via:
```
pip install -r requirements.txt
```
- From there, simply run uvicorn api:app --reload, and navigate to localhost:8000, where you will have access to the FastAPI Swagger UI to utilize each endpoint.

# Schema
- The databases schema is as follows, and are used within the 5 endpoints to modify the database

| Column      | Type     | Constraints               | Description              |
|-------------|----------|---------------------------|--------------------------|
| id          | INTEGER  | PRIMARY KEY, NOT NULL     | Unique task identifier   |
| task        | TEXT     | task TEXT                 | Task details             |
| due_date    | DATE     | DATE NOT NULL             | Due date (YYYY-MM-DD)    |

This schema is restricted further by the implementation of the api, which does not allow task to be less than or greater than a given size range

# Data Model and Relationships

### Task (Create Task/Update Task)

| Field     | Type | Required | Constraints                                         | Description              |
|-----------|------|----------|-----------------------------------------------------|--------------------------|
| due_date  | date | Yes      | Format: YYYY-MM-DD, range: 0001-01-01 to 9999-12-31 | Task due date            |
| task      | str  | Yes      | min_length=1, max_length=255                        | Task description         |

---

### TaskGrabber (Get Task)

| Field     | Type | Required | Constraints                                         | Description              |
|-----------|------|----------|-----------------------------------------------------|--------------------------|
| id        | int  | Yes      | Range: 1 to 2^63 - 1 (SQLite INTEGER max)           | Unique task ID           |
| due_date  | date | Yes      | Format: YYYY-MM-DD, range: 0001-01-01 to 9999-12-31 | Task due date            |
| task      | str  | Yes      | min_length=1, max_length=255                        | Task description         |

---

### TaskPatch (Update Model)

| Field     | Type | Required | Constraints                                        | Description              |
|-----------|------|----------|----------------------------------------------------|--------------------------|
| due_date  | date | No       | Format: YYYY-MM-DD, range: 0001-01-01 → 9999-12-31 | Updated due date         |
| task      | str  | No       | min_length=1, max_length=255                       | Updated task text        |

## Relationships 
- The Project Utilizes 5 different endpoints for each HTTP request type: Post, Get, Head, Put, Delete

- Post utilizes the create_tasks() function, taking in a task object which contains only the due date and task string fields to create a new entry in the DB

- Get uses the get_tasks() function, and takes in an integer for ID, to find the tasks that correspond to a relevant ID 

- Both utilize Task Grabber as a response model, ensuring that they return the ID, Due Date, and Task

- Patch uses the patch_task() function, and takes in an integer ID value (between 1 and 9223372036854775807 inclusive) and a taskPatch object, allowing optional entries for updating for due_date and task, but requiring at least one for successful patching

- Put uses the put_tasks() function, again with a bounded ID value and a normal task object, requiring both values to update as per how PUT requests operate

- Delete uses the delete_tasks() function, which takes in solely the bounded ID to find and delete the values 

- Patch and Put both return the Task Grabber objects, while Delete only returns a success code of 204
