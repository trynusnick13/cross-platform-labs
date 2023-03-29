from typing import Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import models
import schemas


def get_movie(db: Session, movie_id: int):
    return db.query(models.Movies).filter(models.Movies.id == movie_id).first()


def get_movie_by_name(db: Session, name: str):
    return db.query(models.Movies).filter(models.Movies.name == name).first()


def get_movies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Movies).offset(skip).limit(limit).all()


def create_movie(db: Session, movie: schemas.Movie):
    db_movie = models.Movies(
        name=movie.name,
        director=movie.director,
        genre=movie.genre,
        date=movie.date
    )
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)

    return db_movie

def delete_movie(db: Session, movie_id: int) -> int:
    db.query(models.Movies).filter(models.Movies.id == movie_id).delete()
    db.commit()

    return movie_id

def update_movie(db: Session, movie: schemas.Movie, movie_id: int) -> Optional[schemas.Movie]:
    try:
        old_movie = get_movie(db=db, movie_id=movie_id)
        old_movie.date = movie.date
        old_movie.director = movie.director
        old_movie.genre = movie.genre
        old_movie.name = movie.name
        db.add(old_movie)
        db.commit()
        db.refresh(old_movie)
    except Exception as err:
        return None

    return old_movie