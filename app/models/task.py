from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class TaskORM(Base):
    __tablename__ = 'tasks'

    text: Mapped[str]
    status: Mapped[bool] = mapped_column(default=False)