from app import app
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy(app)

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)


class Payments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    payer = db.Column(db.String(50))
    payer_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
    involved = db.Column(db.String, nullable=False)   # comma separated string of names


with app.app_context():
    # db.reflect()
    # db.drop_all()
    db.create_all()