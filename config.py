import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config(object):
    SECRET_KEY = os.environ["SECRET_KEY"] or "that-is-really-strong-key"
    # SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "app.db")
    PSQL_USER = os.environ["PSQL_USER"]
    PSQL_PW = os.environ["PSQL_PW"]
    DB_NAME = os.environ["DB_NAME"]
    PSQL_HOST = os.environ["PSQL_HOST"]
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{user}:{pw}@{host}:5432/{db}".format(
        user=PSQL_USER, pw=PSQL_PW, host=PSQL_HOST, db=DB_NAME
    ) 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BOOKS_PER_PAGE = 5