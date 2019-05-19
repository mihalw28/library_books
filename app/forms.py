from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError

from app.models import Book, Author, Category


class AddBook(FlaskForm):
    title = StringField("Tytuł książki", validators=[DataRequired()])
    author = StringField(
        "Autor/Autorzy",
        validators=[DataRequired()],
        description='Np. "Elon Musk, Jeff Bezos"',
    )
    category = StringField(
        "Kategoria", validators=[DataRequired()], description="Przynajmniej jedna kategoria."
    )
    description = TextAreaField("Opis", validators=[DataRequired()])
    submit = SubmitField("Dodaj do biblioteki!")


class ImportBooks(FlaskForm):
    intitle = StringField("Tytuł książki")
    inauthor = StringField("Autor")
    inpublisher = StringField("Wydawca")
    subject = StringField("Kategoria")
    isbn = StringField("ISBN")
    submit = SubmitField("Zatwierdź dane.")


class FilterBooks(FlaskForm):
    filter_a = StringField("Autor")
    filter_c = StringField("Kategoria")
    submit = SubmitField("Filtruj")
