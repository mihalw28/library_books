from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError

from app.models import Book


class AddBook(FlaskForm):
    title = StringField("Tytuł kasiążki", validators=[DataRequired()])
    author = StringField("Autor", validators=[DataRequired()])
    category = StringField("Kategoria", validators=[DataRequired()])
    description = TextAreaField("Opis", validators=[DataRequired()])
    submit = SubmitField("Dodaj do biblioteki!")

    def validate_book_title(self, title):
        book = Book.query.filter_by(title=title.data).first()
        if book is not None:
            raise ValidationError("Książka o takim tytule już znajduje się już w bazie.")


class ImportBooks(FlaskForm):
    intitle = StringField("Tytuł książki")
    inauthor = StringField("Autor")
    inpublisher = StringField("Wydawca")
    subject = StringField("Kategoria")
    isbn = StringField("ISBN")
    submit = SubmitField("Zatwierdź")


# To do:
# class ShowAllBooks(FlaskForm):
