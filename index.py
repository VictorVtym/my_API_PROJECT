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

# source .venv/Scripts/activate
# uvicorn index:app --port 8000 --reload

tasks: list[TaskShema] = []

@app.get("/tasks")
async def read_tasks():
    return tasks


@app.post("/postdata")
async def postdata(payload: TaskCreateShema):
    new_task = TaskShema(id=str(uuid4), text=payload.text, status=False)
    tasks.append(new_task)
    return {"status": "success", "task": new_task}

#async def postdata(payload: ItemPayload):
#    return {"message": "Товар теперь создан", "Имя пользователя": payload.name}