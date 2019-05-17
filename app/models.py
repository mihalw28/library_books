from app import db


book_author_helper = db.Table(
    "book_author",
    db.Column("author_id", db.Integer, db.ForeignKey("author.id"), primary_key=True),
    db.Column("book_id", db.Integer, db.ForeignKey("book.id"), primary_key=True),
)


book_category_helper = db.Table(
    "book_category",
    db.Column("book_id", db.Integer, db.ForeignKey("book.id"), primary_key=True),
    db.Column("category_id", db.Integer, db.ForeignKey("category.id"), primary_key=True),
)


class Book(db.Model):
    __tablename__ = "book"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)

    book_authors = db.relationship(
        "Author",
        secondary=book_author_helper,
        lazy="subquery",
        backref=db.backref("books"),
    )

    book_categories = db.relationship(
        "Category",
        secondary=book_category_helper,
        lazy="subquery",
        backref=db.backref("books", lazy=True),
    )

    def __init__(self, title, description, book_authors=[], book_categories=[]):
        self.title = title
        self.description = description
        self.book_authors = book_authors
        self.book_categories = book_categories

    def __repr__(self):
        return f"{self.__class__.__name__}({self.title})"

    def __str__(self):
        return f"{self.title}"


class Author(db.Model):
    __tablename__ = "author"
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.full_name})"

    def __str__(self):
        return f"{self.full_name}"


class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.category_name})"

    def __str__(self):
        return f"{self.category_name}"
