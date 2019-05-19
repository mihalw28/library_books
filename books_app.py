from app import app as application, db
from app.models import Author, Book, Category


@application.shell_context_processor
def make_shell_context():
    return {"db": db, "Author": Author, "Book": Book, "Category": Category}
