import os
import sqlite3
from tkinter import (
    NO,
    Button,
    StringVar,
    Tk,
    Toplevel,
    ttk,
    LabelFrame,
    Label,
    Entry,
    END,
    CENTER,
    W,
    E,
)

import requests

API_URL = os.getenv("API_URL", "http://0.0.0.0:8000")


class Movie:
    # connection dir property
    db_name = "database.db"

    def __init__(self, window):
        # Initializations
        self.wind = window
        self.wind.title("Movies Library")

        # Creating a Frame Container
        frame = LabelFrame(self.wind, text="Add new Movie")
        frame.grid(row=0, column=0, columnspan=6, pady=20)

        # Name Input
        Label(frame, text="Name: ").grid(row=1, column=0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row=1, column=1)

        # Director Input
        Label(frame, text="Director: ").grid(row=2, column=0)
        self.director = Entry(frame)
        self.director.grid(row=2, column=1)

        # Genre Input
        Label(frame, text="Genre: ").grid(row=3, column=0)
        self.genre = Entry(frame)
        self.genre.grid(row=4, column=1)

        # Date Input
        Label(frame, text="Date: ").grid(row=4, column=0)
        self.date = Entry(frame)
        self.date.grid(row=5, column=1)

        # Button Add Movie
        ttk.Button(frame, text="Add Movie", command=self.add_movie).grid(
            row=6, columnspan=2, sticky=W + E
        )

        # Output Messages
        self.message = Label(text="", fg="red")
        self.message.grid(row=6, column=0, columnspan=2, sticky=W + E)

        # Table
        self.tree = ttk.Treeview(height=10, columns=4)
        self.tree["columns"] = ("id", "name", "director", "genre", "date")

        self.tree.grid(row=7, column=0, columnspan=4)
        self.tree.column("#0", width=0, stretch=NO)
        self.tree.heading("#0", text="", anchor=CENTER)
        self.tree.heading("id", text="ID", anchor=CENTER)
        self.tree.heading("name", text="Name", anchor=CENTER)
        self.tree.heading("director", text="Director", anchor=CENTER)
        self.tree.heading("genre", text="Genre", anchor=CENTER)
        self.tree.heading("date", text="Date", anchor=CENTER)

        # Buttons
        ttk.Button(text="DELETE", command=self.delete_movie, width=10).grid(
            row=4, column=1, sticky=W + E
        )
        ttk.Button(text="EDIT", command=self.edit_movie).grid(
            row=4, column=2, sticky=W + E
        )

        # Filling the Rows
        self.get_movies()

    def get_movies(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        movies: list[dict[str, str]] = requests.get(f"{API_URL}/movies/").json()
        for movie in movies:
            self.tree.insert(
                "",
                0,
                text=movie["id"],
                values=[
                    movie["id"],
                    movie["name"],
                    movie["director"],
                    movie["genre"],
                    movie["date"],
                ],
            )

    # User Input Validation
    def validation(self):
        return len(self.name.get()) != 0 and len(self.director.get()) != 0

    def add_movie(self):
        if self.validation():
            payload = {
                "name": self.name.get(),
                "director": self.director.get(),
                "genre": self.genre.get(),
                "date": self.date.get(),
            }
            movie: dict[str, str] = requests.post(
                f"{API_URL}/movies/", json=payload
            ).json()
            self.message["text"] = "Movie {} added Successfully".format(self.name.get())
            self.name.delete(0, END)
            self.director.delete(0, END)
            self.genre.delete(0, END)
            self.date.delete(0, END)

        self.get_movies()

    def delete_movie(self):
        self.message["text"] = ""
        try:
            self.tree.item(self.tree.selection())["text"]
        except IndexError as e:
            self.message["text"] = "Please select a Record"
            return
        self.message["text"] = ""
        id = self.tree.item(self.tree.selection())["text"]
        response = requests.delete(f"{API_URL}/movies/{id}").json()
        self.message["text"] = "Record {} deleted Successfully".format(id)
        self.get_movies()

    def edit_movie(self):
        self.message["text"] = ""
        try:
            self.tree.item(self.tree.selection())["values"]
        except IndexError as e:
            self.message["text"] = "Please, select Record"
            return
        id = self.tree.item(self.tree.selection())["text"]
        old_name = self.tree.item(self.tree.selection())["values"][1]
        old_director = self.tree.item(self.tree.selection())["values"][2]
        old_genre = self.tree.item(self.tree.selection())["values"][3]
        old_date = self.tree.item(self.tree.selection())["values"][4]
        self.edit_wind = Toplevel()
        self.edit_wind.title = "Edit Movie"
        # Old Name
        Label(self.edit_wind, text="Old Name:").grid(row=0, column=1)
        Entry(
            self.edit_wind,
            textvariable=StringVar(self.edit_wind, value=old_name),
            state="readonly",
        ).grid(row=0, column=2)
        # New Name
        Label(self.edit_wind, text="New Name:").grid(row=1, column=1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row=1, column=2)

        # Old Director
        Label(self.edit_wind, text="Old Director:").grid(row=3, column=1)
        Entry(
            self.edit_wind,
            textvariable=StringVar(self.edit_wind, value=old_director),
            state="readonly",
        ).grid(row=3, column=2)
        # New Director
        Label(self.edit_wind, text="New Director:").grid(row=4, column=1)
        new_director = Entry(self.edit_wind)
        new_director.grid(row=4, column=2)

        # Old Genre
        Label(self.edit_wind, text="Old Genre:").grid(row=5, column=1)
        Entry(
            self.edit_wind,
            textvariable=StringVar(self.edit_wind, value=old_genre),
            state="readonly",
        ).grid(row=5, column=2)
        # New Genre
        Label(self.edit_wind, text="New Genre:").grid(row=6, column=1)
        new_genre = Entry(self.edit_wind)
        new_genre.grid(row=6, column=2)

        # Old Date
        Label(self.edit_wind, text="Old Date:").grid(row=7, column=1)
        Entry(
            self.edit_wind,
            textvariable=StringVar(self.edit_wind, value=old_date),
            state="readonly",
        ).grid(row=7, column=2)
        # New Date
        Label(self.edit_wind, text="New Date:").grid(row=8, column=1)
        new_date = Entry(self.edit_wind)
        new_date.grid(row=8, column=2)

        Button(
            self.edit_wind,
            text="Update",
            command=lambda: self.update(
                id=id,
                name=new_name.get(),
                director=new_director.get(),
                genre=new_genre.get(),
                date=new_date.get(),
            ),
        ).grid(row=9, column=2, sticky=W)
        self.edit_wind.mainloop()

    def update(self, id: int, name: str, director: str, genre: str, date: str):
        payload = {
            "name": name,
            "director": director,
            "genre": genre,
            "date": date,
        }
        movie: dict[str, str] = requests.put(
            f"{API_URL}/movies/{id}", json=payload
        ).json()
        print(movie)
        self.edit_wind.destroy()
        self.get_movies()


if __name__ == "__main__":
    window = Tk()
    application = Movie(window)
    window.mainloop()
