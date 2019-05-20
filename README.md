# library_books 

library_books repo contains an app written in Python for managing books. Created for job application process.

## Project guideline

Using any Python framework create an app for managing collection of books.
1. Create database objects with specific relations beetween books, authors and categories.
Example of data source [here](https://www.googleapis.com/books/v1/volumes?q=Hobbit).
2. Books should have descriptions excetpt categories and authors.
3. App should contain three veiws:
    * List of books with ability for filtering based on author and category. List of books should also contain descriptions, authors and cateogries.
    * Import books based on key words from [API](https://www.google.com/url?q=https://developers.google.com/books/docs/v1/using%23WorkingVolumes&). Imported books must be saved in a way, that allows to query all books from database (including added manually)
    * Form to add book manually.
4. Deploy app on public server.
5. Layout of the pages is not important.

## Made using:
  * Flask
  * SQLAlchemy
  * WTForms
  * Bootstrap
  * deployed on AWS (Elastic Beanstalk + PostgreSQL)

## License

MIT © [Michał Waszak](https://github.com/mihalw28)
