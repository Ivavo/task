from flask_sqlalchemy import SQLAlchemy

SESSION_OPTIONS = {
    'autoflush': False,
    'autocommit': False
}

db = SQLAlchemy(session_options=SESSION_OPTIONS)


def init(app):
    db.init_app(app)
