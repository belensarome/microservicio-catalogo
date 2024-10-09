from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os
from app.config import config
from app.route import RouteApp

db = SQLAlchemy()
migrate = Migrate()


def create_app() -> Flask:
    app_context = os.getenv("FLASK_CONTEXT")
    app = Flask(__name__)

    f = config.factory(app_context if app_context else 'testing')
    app.config.from_object(f)

    route = RouteApp()
    route.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    return app