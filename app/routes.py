import json

import requests
from flask import flash, redirect, render_template, url_for, session

from app import app, db
from app.forms import AddBook, ImportBooks
from app.models import Author, Book, Category


@app.route("/")
@app.route("/index")
def index():
    books = Book.query.all()
    return render_template("index.html", title="Book list")


@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    """A function that adds a new book to library with data from AddBook form."""
    form = AddBook()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        author = form.author.data.split(", ")  # For more than one author.
        category = form.category.data.split(", ")  # The same.
        add_to_db(title, description, author, category)
        flash(
            "Wygląda na to, że wszystko poszło dobrze i dodałaś/eś książkę do \
            biblioteki."
        )
        return redirect(url_for("index"))
    return render_template("add_book.html", title="Add new book", form=form)


@app.route("/import_books", methods=["GET", "POST"])
def import_books():
    """A function that creates url based on data from user typed in ImportBooks form."""
    form = ImportBooks()
    base_url = "https://www.googleapis.com/books/v1/volumes?q="
    new_list = []
    keys = ["intitle", "inauthor", "inpublisher", "subject", "isbn"]
    if form.validate_on_submit():
        title = form.intitle.data
        author = form.inauthor.data
        publisher = form.inpublisher.data
        subject = form.subject.data
        isbn = form.isbn.data

        list_str = [title, author, publisher, subject, isbn]
        for val, key in zip(list_str, keys):
            if val == "":
                del val, key
            else:
                new_list.append(f"{key}:{val}")
        url_rest = "+".join(new_list)
        url = base_url + url_rest
        session["url"] = url
    return render_template("import_book.html", title="import", form=form)


@app.route("/import_all", methods=["GET", "POST"])
def import_all():
    """A function that saved books to db based on url from import_books."""
    response = requests.get(session["url"])
    result = response.json()
    if result['totalItems'] == 0:
        flash("Okazuje się, że żadne książki nie spełniają podanych kryteriów. Spróbuj jeszcze raz.")
    else:
        how_many = len(result["items"])
        for i in range(how_many):
            info = result["items"][i]["volumeInfo"]
            title = info["title"]
            try:
                authors = info["authors"]
            except KeyError:
                authors = "" 
            try:
                subject = info["categories"]
            except KeyError: 
                subject = ""
            try:
                description = info["description"]
            except KeyError:
                description = ""
            add_to_db(title, description, authors, subject)
        flash(f"Wygląda na to, że wszystko dobrze poszło i dodałaś/eś {how_many} książek do biblioteki.")
    # session.clear()
    return redirect(url_for("import_books"))


def add_to_db(title, description, author, category):
    """This function solves issues with input data if there are many authors or categories."""
    au_list = []
    cat_list = []
    book = Book(title=title, description=description)
    for auth in author:
        au = Author(full_name=auth)
        db.session.add(au)
        au_list.append(au)
    for cats in category:
        cat = Category(category_name=cats)
        db.session.add(cat)
        cat_list.append(cat)
    book.book_authors.extend(au_list)
    book.book_categories.extend(cat_list)
    db.session.commit()
    return