from app import app
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy(app)

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)


with app.app_context():
    db.create_all()