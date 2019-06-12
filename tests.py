import unittest
from flask_testing import TestCase
from app import db
from flask import current_app, url_for, Flask, request
from app.models import Book, Author, Category
from config import Config
from flask_sqlalchemy import SQLAlchemy


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"


class TestBase(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config.from_object(TestConfig)
        db = SQLAlchemy(app)
        return app

    def setUp(self):
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestModels(TestBase):
    def test_author_model(self):
        """
        Test adding an author & count number of records in Author table.
        """
        author = Author(full_name="Ernest Hemingway")
        db.session.add(author)
        db.session.commit()
        self.assertEqual(Author.query.first().full_name, "Ernest Hemingway")
        self.assertEqual(Author.query.count(), 1)

    def test_category_model(self):
        """
        Test adding a category & count number of records in Category table.
        """
        category = Category(category_name="War novel")
        db.session.add(category)
        db.session.commit()
        self.assertEqual(Category.query.first().category_name, "War novel")
        self.assertEqual(Category.query.count(), 1)

    def test_book_model(self):
        """
        Test adding a book & number of records in Book table.
        """
        author = Author(full_name="Erenest Hemingway")
        additional_author = Author(full_name="My Name")
        category = Category(category_name="War novel")
        additional_category = Category(category_name="WWII")
        book = Book(
            title="For Whom the Bell Toll",
            description="It tells the story of Robert Jordan.",
            book_categories=[category],
            book_authors=[author],
        )
        db.session.add(book)
        db.session.commit()
        book.book_authors.append(additional_author)
        book.book_categories.append(additional_category)
        db.session.commit()
        self.assertEqual(Book.query.count(), 1)
        self.assertEqual(Book.query.first().title, "For Whom the Bell Toll")
        self.assertEqual(
            Book.query.first().description, "It tells the story of Robert Jordan."
        )
        self.assertEqual(
            Book.query.first().book_categories, [category, additional_category]
        )
        self.assertEqual(Book.query.first().book_authors, [author, additional_author])


if __name__ == "__main__":
    unittest.main(verbose=2)
