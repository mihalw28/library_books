from app import app, db
from app.models import Author, Book, Category


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "Author": Author, "Book": Book, "Category": Category}
