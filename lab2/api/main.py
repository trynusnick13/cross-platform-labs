from fastapi import Depends, FastAPI, HTTPException, Response
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/movies/", response_model=schemas.Movie)
def create_movie(movie: schemas.Movie, db: Session = Depends(get_db)):
    db_movie = crud.get_movie_by_name(db, name=movie.name)
    if db_movie:
        raise HTTPException(status_code=400, detail="Name already Exists")

    return crud.create_movie(db=db, movie=movie)


@app.get("/movies/", response_model=list[schemas.Movie])
def read_movies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    movies = crud.get_movies(db, skip=skip, limit=limit)

    return movies


@app.get("/movies/{movie_id}", response_model=schemas.Movie)
def read_movie(movie_id: int, db: Session = Depends(get_db)):
    db_movie = crud.get_movie(db, movie_id=movie_id)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    return db_movie

@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db)) -> dict:
    db_movie = crud.delete_movie(db, movie_id=movie_id)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    return {"deleted": movie_id}

@app.put("/movies/{movie_id}", response_model=schemas.Movie)
def update_movie(movie_id: int, movie: schemas.Movie, db: Session = Depends(get_db)):
    updated_movie = crud.update_movie(db=db, movie=movie, movie_id=movie_id)
    if updated_movie is None:
        raise HTTPException(status_code=404, detail="Movie with this name already exists")

    return updated_movie

