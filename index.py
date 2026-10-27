from fastapi import FastAPI, Form
from pydantic import BaseModel
from fastapi.responses import FileResponse
from uuid import uuid4

app = FastAPI()

@app.get("/")
async def welcome() -> dict:
    return FileResponse("templates/main.html")


class TaskShema(BaseModel):
    id: str
    text: str
    status: bool


class TaskCreateShema(BaseModel):
    text: str


class TaskUpdateShema(BaseModel):
    text: str | None = None
    status: bool | None = None

# source .venv/Scripts/activate
# uvicorn index:app --port 8000 --reload
# git push -u origin main

tasks: list[TaskShema] = []


@app.get("/tasks")
async def read_tasks():
    return tasks


@app.post("/tasks")
async def postdata(payload: TaskCreateShema):
    new_task = TaskShema(id=str(uuid4()), text=payload.text, status=False)
    tasks.append(new_task)
    return {"status": "success", "task": new_task.text}


@app.patch("/tasks/{task_id}")
def update_task(task_id: str, payload: TaskUpdateShema):
    for task in tasks:
        if task.id == task_id:
            if payload.text:
                task.text = payload.text
            if payload.status is not None:
                task.status = payload.status

            return task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: str):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)

            return task