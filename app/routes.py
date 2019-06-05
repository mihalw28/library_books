import json

import requests
from flask import flash, redirect, render_template, request, session, url_for

from app import app, db
from app.forms import AddBook, FilterBooks, ImportBooks
from app.models import Author, Book, Category


@app.route("/")
def first_redirection():  # Method not allowed for '/' route, hence this redirection.
    return redirect(url_for("index"))


@app.route("/index", methods=["GET", "POST"])
def index():
    form = FilterBooks()
    if form.validate_on_submit():
        filter_a_str = form.filter_a.data
        filter_c_str = form.filter_c.data
        filter_list = [filter_a_str, filter_c_str]
        session["fl_lst"] = filter_list
        return redirect(url_for("filtered_books"))
    return render_template("index.html", title="Filter", form=form)


@app.route("/filtered_books", methods=["GET"])
def filtered_books():
    try:
        fl = session["fl_lst"]
    except:
        pass
    page = request.args.get("page", 1, type=int)
    if fl[0] or fl[1]:
        bks = query_books(fl)
    else:
        bks = Book.query.order_by(Book.title)
    if len(bks.all()) == 0:
        flash(
            "Niestety żadne książki z biblioteki nie spełniają kryteriów filtrowania.",
            "error",
        )
    books = bks.paginate(page, app.config["BOOKS_PER_PAGE"], False)
    next_page = url_for("filtered_books", page=books.next_num) if books.has_next else None
    prev_page = url_for("filtered_books", page=books.prev_num) if books.has_prev else None
    return render_template(
        "filtered_books.html",
        title="Filtered",
        books=books,
        next_page=next_page,
        prev_page=prev_page,
    )


@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    """A function that adds a new book to library with data from AddBook form."""
    form = AddBook()
    if form.validate_on_submit():
        title_str = form.title.data
        description_str = form.description.data
        a_list_str = [auth.strip() for auth in form.author.data.split(",")]
        c_list_str = form.category.data.split(", ")
        add_to_db(title_str, description_str, a_list_str, c_list_str)
        flash(
            "Wygląda na to, że wszystko poszło dobrze i dodałaś/eś książkę do \
            biblioteki. Możesz ją teraz wyszukać w zakładce 'dostępne' lub dodać kolejną.",
            "success",
        )
        return redirect(url_for("add_book"))
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
        new_list = [f"{key}:{val}" for val, key in zip(list_str, keys) if val != ""]  # more pythonic than standard for loop
        url_rest = "+".join(new_list)
        url = base_url + url_rest
        session["url"] = url
        flash(
            "Wpisane przez Ciebie dane zostały zatwierdzone. Teraz możesz importować.",
            "success",
        )
        return redirect(url_for("import_books"))
    return render_template("import_book.html", title="Import", form=form)


@app.route("/import_all", methods=["GET", "POST"])
def import_all():
    """A function that saved books to db based on url from import_books."""
    response = requests.get(session["url"])
    result = response.json()
    session.clear()
    if result["totalItems"] == 0:
        flash(
            "Okazuje się, że żadne książki ze zbiorów Google nie spełniają Twoich kryteriów. Spróbuj jeszcze raz.",
            "error",
        )
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
        flash(
            f"Wygląda na to, że wszystko dobrze poszło i dodałaś/eś {how_many} książek do biblioteki.",
            "success",
        )
    return redirect(url_for("import_books"))


def add_to_db(title, description, a_strings, c_strings):
    """This function solves issues with data if there are many authors or categories."""
    a_objects = [Author(full_name=auth) for auth in a_strings]
    c_objects = [Category(category_name=cat) for cat in c_strings]
    book = Book(
        title=title,
        description=description,
        book_authors=a_objects,
        book_categories=c_objects,
    )
    db.session.add(book)
    db.session.commit()
    return


def query_books(list_args):
    """This function generates books query, also with user filters."""
    auth_query = Book.book_authors.any(Author.full_name.contains(list_args[0]))
    cat_query = Book.book_categories.any(Category.category_name.contains(list_args[1]))
    bks = Book.query.filter(auth_query, cat_query).order_by(Book.title)
    return bks
