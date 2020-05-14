from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from profiler_server.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from .routes import routes
