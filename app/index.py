from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.models.base import Base
from app.db.session import engine
from app.api.routers.task import router as task_router


## это нужно для того, чтобы таблицы создавались при подключении БД
@asynccontextmanager
async def lifespan(_: FastAPI):
    print("Приложение запущено")
    Base.metadata.create_all(bind=engine)
    yield
    print("Приложение остановлено")


app = FastAPI(lifespan=lifespan)
app.include_router(router=task_router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def welcome() -> dict:
    return FileResponse("app/templates/main.html")


# source .venv/Scripts/activate
# uvicorn index:app --port 8000 --reload (основоной файл index.py в корне проекта)
# uvicorn app.index:app --port 8000 --reload  (основной файл index.py в папке app)
# git push -u origin main
# docker run --name pg_container -e POSTGRES_PASSWORD=admin -d -p 5432:5432 postgres
# docker exec -it pg_container psql -U postgres
# \q или Ctrl + D
# docker stop pg-container
# docker compose down -v
# docker compose up --build
# http://localhost:8080/docs