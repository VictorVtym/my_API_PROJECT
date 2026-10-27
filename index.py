from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from pydantic import BaseModel
from fastapi.responses import FileResponse
from uuid import uuid4
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, Session

DATABASE_URL = "postgresql+psycopg://postgres:admin@127.0.0.1:5432/postgres"
#DATABASE_URL = "postgresql+asyncpg://postgres:admin@127.0.0.1:5432/postgres"

engine = create_engine(DATABASE_URL)
Sessionlocal = sessionmaker[Session](bind=engine)


class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))


class TaskORM(Base):
    __tablename__ = 'tasks'

    text: Mapped[str]
    status: Mapped[bool] = mapped_column(default=False)


@asynccontextmanager
async def lifespan(_: FastAPI):
    print("Приложение запущено")
    Base.metadata.create_all(bind=engine)
    yield
    print("Приложение остановлено")


app = FastAPI(lifespan=lifespan)

@app.get("/")
def welcome() -> dict:
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
# docker run --name pg_container -e POSTGRES_PASSWORD=admin -d -p 5432:5432 postgres
# docker exec -it pg_container psql -U postgres
# \q или Ctrl + D
# docker stop pg-container

tasks: list[TaskShema] = []


@app.get("/tasks")
def read_tasks():
    return tasks


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def postdata(payload: TaskCreateShema):
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


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)

            return task