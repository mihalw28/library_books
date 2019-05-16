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

    def __repr__(self):
        return f"<Book {self.title}>"


class Author(db.Model):
    __tablename__ = "author"
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String)

    def __repr__(self):
        return f"<Author {self.full_name}>"


class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String)

    def __repr__(self):
        return f"<Category {self.category_name}>"
