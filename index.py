from fastapi import FastAPI, Form
from pydantic import BaseModel
from fastapi.responses import FileResponse

app = FastAPI()

@app.get("/")
async def welcome() -> dict:
    return FileResponse("templates/main.html")

class ItemPayload(BaseModel):
    name: str
    age: int

# source .venv/Scripts/activate
# uvicorn index:app --port 8000 --reload

@app.post("/postdata")
async def postdata(payload: ItemPayload):
    return {"message": "Товар теперь создан", "Имя пользователя": payload.name}