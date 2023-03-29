from sqlalchemy import Boolean, Column, Date, Integer, String

from database import Base


class Movies(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    director = Column(String)
    genre = Column(String)
    date = Column(String)
