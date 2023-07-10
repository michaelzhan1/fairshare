from app import app
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy(app)

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False, unique=True)


class Payments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    description = db.Column(db.String)
    amount = db.Column(db.Float, nullable=False)
    payer = db.Column(db.String(50))
    payer_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
    involved = db.Column(db.String, nullable=False)   # comma separated string of names
    date = db.Column(db.DateTime, default=db.func.current_timestamp())  # returns in 'Mon, 10 Jul 2023 15:26:26 GMT' format after jsonify


class Groups(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.String(6), nullable=False, unique=True)


with app.app_context():
    # db.reflect()
    # db.drop_all()
    db.create_all()