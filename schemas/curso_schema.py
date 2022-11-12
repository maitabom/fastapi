from typing import Optional

from pydantic import BaseModel


class Curso(BaseModel):
    id: Optional[int]
    titulo: str
    aulas: int
    horas: int

    class Config:
        orm_mode = True
