from flask import Flask, session
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from config import Config

application = app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)
bootstrap = Bootstrap(app)

from app import models, routes

if __name__ == "__main__":
    application.run(debug=False)
