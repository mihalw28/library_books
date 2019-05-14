from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class AddBook(FlaskForm):
    title = StringField("Tytuł kasiążki", validators=[DataRequired()])
    author = StringField("Autor", validators=[DataRequired()])
    category = StringField("Kategoria", validators=[DataRequired()])
    description = StringField("Opis", validators=[DataRequired()])
    submit = SubmitField("Dodaj do biblioteki!")


class ImportBooks(FlaskForm):
    intitle = StringField("Tytuł książki")
    inauthor = StringField("Autor")
    inpublisher = StringField("Wydawca")
    subject = StringField("Kategoria")
    isbn = StringField("ISBN")
    submit = SubmitField("Szukaj")


# class ShowAllBooks(FlaskForm):