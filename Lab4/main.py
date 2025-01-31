from fastapi import FastAPI, HTTPException, Depends, Request
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
import os


load_dotenv()

app = FastAPI()


API_KEY = os.getenv("LAB4_API_KEY")
if not API_KEY:
    raise RuntimeError("API key not found. Please set it in the .env file.")


def verify_api_key(request: Request):
    api_key = request.headers.get("Authorization")
    if api_key != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="Invalid API Key")


class Task(BaseModel):
    task_id: int
    task_title: str
    task_desc: Optional[str] = None
    is_finished: bool = False

task_db = [
    {"task_id": 1, "task_title": "Laboratory Activity", "task_desc": "Create Lab Act 2", "is_finished": False}
]


@app.get("/apiv1/tasks/{task_id}")
def read_task_v1(task_id: int):
    for task in task_db:
        if task["task_id"] == task_id:
            return {"status": "ok", "task": task}
    raise HTTPException(status_code=404, detail="Task not found.")

@app.post("/apiv1/tasks", dependencies=[Depends(verify_api_key)])
def create_task_v1(task: Task):
    if any(t['task_id'] == task.task_id for t in task_db):
        raise HTTPException(status_code=400, detail="Task ID already exists.")
    task_db.append(task.dict())
    return {"status": "ok", "created_task": task}, 201

@app.patch("/apiv1/tasks/{task_id}", dependencies=[Depends(verify_api_key)])
def update_task_v1(task_id: int, task: Task):
    for idx, t in enumerate(task_db):
        if t["task_id"] == task_id:
            task_db[idx].update({k: v for k, v in task.dict().items() if v is not None})
            return {"status": "ok", "updated_task": task_db[idx]}, 204
    raise HTTPException(status_code=404, detail="Task not found.")

@app.delete("/apiv1/tasks/{task_id}", dependencies=[Depends(verify_api_key)])
def delete_task_v1(task_id: int):
    for idx, task in enumerate(task_db):
        if task["task_id"] == task_id:
            removed_task = task_db.pop(idx)
            return {"status": "ok", "removed_task": removed_task}, 204
    raise HTTPException(status_code=404, detail="Task not found.")


@app.get("/apiv2/tasks/{task_id}", dependencies=[Depends(verify_api_key)])
def read_task_v2(task_id: int):
    for task in task_db:
        if task["task_id"] == task_id:
            return {"status": "ok", "task": task}
    raise HTTPException(status_code=404, detail="Task not found.")

@app.post("/apiv2/tasks", dependencies=[Depends(verify_api_key)])
def create_task_v2(task: Task):
    if any(t['task_id'] == task.task_id for t in task_db):
        raise HTTPException(status_code=400, detail="Task ID already exists.")
    task_db.append(task.dict())
    return {"status": "ok", "created_task": task}, 201

@app.patch("/apiv2/tasks/{task_id}", dependencies=[Depends(verify_api_key)])
def update_task_v2(task_id: int, task: Task):
    for idx, t in enumerate(task_db):
        if t["task_id"] == task_id:
            task_db[idx].update({k: v for k, v in task.dict().items() if v is not None})
            return {"status": "ok", "updated_task": task_db[idx]}, 204
    raise HTTPException(status_code=404, detail="Task not found.")

@app.delete("/apiv2/tasks/{task_id}", dependencies=[Depends(verify_api_key)])
def delete_task_v2(task_id: int):
    for idx, task in enumerate(task_db):
        if task["task_id"] == task_id:
            removed_task = task_db.pop(idx)
            return {"status": "ok", "removed_task": removed_task}, 204
    raise HTTPException(status_code=404, detail="Task not found.")
