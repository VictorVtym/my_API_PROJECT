from pydantic import BaseModel, ConfigDict


class TaskShema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    text: str
    status: bool


class TaskCreateShema(BaseModel):
    text: str


class TaskUpdateShema(BaseModel):
    text: str | None = None
    status: bool | None = None