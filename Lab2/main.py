from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional


app = FastAPI()

class Task(BaseModel):
    task_id: int
    task_title: str
    task_desc: Optional[str] = None
    is_finished: bool = False


task_db = [
    {"task_id": 1, "task_title": "Laboratory Activity", "task_desc": "Create Lab Act 2", "is_finished": False}
]


@app.get("/tasks/{task_id}")
def read_task(task_id: int):

    if task_id <= 0:
        return {"error": "Invalid task ID, must be positive."}

    for task in task_db:
        if task["task_id"] == task_id:
            return {"status": "ok", "task": task}
 
    return {"error": "Task not found."}


@app.post("/tasks")
def create_task(task: Task):

    if any(t['task_id'] == task.task_id for t in task_db):
        return {"error": "Task ID already exists."}
    
 
    task_db.append(task.dict())
    return {"status": "ok", "created_task": task}


@app.patch("/tasks/{task_id}")
def update_task(task_id: int, task: Task):

    if task_id <= 0:
        return {"error": "Invalid task ID, must be positive."}
    
 
    for idx, t in enumerate(task_db):
        if t["task_id"] == task_id:
            if task.task_title:
                task_db[idx]["task_title"] = task.task_title
            if task.task_desc:
                task_db[idx]["task_desc"] = task.task_desc
            if task.is_finished is not None:
                task_db[idx]["is_finished"] = task.is_finished
            return {"status": "ok", "updated_task": task_db[idx]}
    

    return {"error": "Task not found."}


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
  
    if task_id <= 0:
        return {"error": "Invalid task ID, must be positive."}
    
   
    for idx, task in enumerate(task_db):
        if task["task_id"] == task_id:
            removed_task = task_db.pop(idx)
            return {"status": "ok", "removed_task": removed_task}
    
   
    return {"error": "Task not found."}
