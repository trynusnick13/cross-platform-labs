from typing import Optional

from pydantic import BaseModel


class Movie(BaseModel):
    id: Optional[int]
    name: str
    director: str
    genre: str
    date: str

    class Config:
        orm_mode = True
