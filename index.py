from uuid import uuid4
from contextlib import asynccontextmanager
from fastapi import FastAPI, status, Depends
from pydantic import BaseModel
from fastapi.responses import FileResponse
from sqlalchemy import create_engine, select
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

## это нужно для того, чтобы таблицы создавались при подключении БД
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

# подключение к БД
def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()


def task_orm_to_model(task_orm: TaskORM) -> TaskShema:
    return TaskShema(id=task_orm.id, text=task_orm.text, status=task_orm.status)


@app.get("/tasks")
def read_tasks(db: Session = Depends(get_db)) -> list[TaskShema]:
    tasks_from_db = db.scalars(select(TaskORM)).all()
    return [task_orm_to_model(task) for task in tasks_from_db]


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_tasks(payload: TaskCreateShema, db: Session = Depends(get_db)) -> TaskShema:
    new_task = TaskORM(text=payload.text, status=False)
    db.add(new_task)
    db.commit()
    return task_orm_to_model(new_task)


@app.patch("/tasks/{task_id}")
def update_task(task_id: str, payload: TaskUpdateShema, db: Session = Depends(get_db)) -> TaskShema:
    task_for_update = db.get(TaskORM, task_id)
    if payload.text:
        task_for_update.text = payload.text
    if payload.status:
        task_for_update.status = payload.status

    db.commit()
    return task_for_update


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id, db: Session = Depends(get_db)) -> None:
    task_for_delete = db.get(TaskORM, task_id)
    db.delete(task_for_delete)
    db.commit()