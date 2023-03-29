import os

import requests
import typer

app = typer.Typer()

API_URL = os.getenv("API_URL", "http://0.0.0.0:8000")


@app.command()
def list_all_movies():
    movies: list[dict[str, str]] = requests.get(f"{API_URL}/movies/").json()
    for movie in movies:
        print(
            f"Name: {movie['name']}, Director: {movie['director']}, "
            f"Genre: {movie['genre']}, Date released: {movie['date']}"
        )


@app.command()
def add_movie(name: str, director: str, genre: str, date: str):
    payload = {
        "name": name,
        "director": director,
        "genre": genre,
        "date": date,
    }
    movie: dict[str, str] = requests.post(f"{API_URL}/movies/", json=payload).json()
    print(movie)


@app.command()
def read_movie(id: int):
    movie: dict[str, str] = requests.get(f"{API_URL}/movies/{id}").json()
    print(movie)


@app.command()
def update_movie(id: int, name: str, director: str, genre: str, date: str):
    payload = {
        "name": name,
        "director": director,
        "genre": genre,
        "date": date,
    }
    movie: dict[str, str] = requests.put(f"{API_URL}/movies/{id}", json=payload).json()
    print(movie)


@app.command()
def delete_movie(id: int):
    response: dict[str, str] = requests.delete(f"{API_URL}/movies/{id}").json()
    print(response)


if __name__ == "__main__":
    app()
