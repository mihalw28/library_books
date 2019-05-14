from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import AddBook, ImportBooks
import json
import requests


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", title="Book list")


@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    form = AddBook()
    if form.validate_on_submit():
        flash(
            "Wygląda na to, że wszystko poszło dobrze i dodałaś/eś książkę do \
            biblioteki."
        )
        return redirect(url_for("index"))
    return render_template("add_book.html", title="Add new book", form=form)


@app.route("/import_books", method=["GET", "POST"])
def import_books():
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
    response = requests.get(base_url + url_rest)
    result = json.loads(response.text)
    return result


def clean_json(result):
    """
    Cleaning raw json results to extract 3 parameters.
    """
    for i in range(len(result["items"])):
        info = result['items'][i]['volumeInfo']
        title = info['title']
        authors = info["authors"]
        if "categories" in info:
            subject = info["categories"]
        else: 
            subject = ""
        if "description" in info:
            description = info["description"]
        else:
            description = ""
        return title, authors, subject, description


