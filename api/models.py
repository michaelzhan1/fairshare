from app import app
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy(app)

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)


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
    # dummy_group = Groups(group_id='aaaaaa')
    # db.session.add(dummy_group)
    # dummy_people = ['a', 'b', 'c', 'd', 'e']
    # for person in dummy_people:
    #     dummy_person = People(group_id='aaaaaa', name=person)
    #     db.session.add(dummy_person)
    # dummy_payments = [
    #     {'description': 'pizza', 'amount': 20, 'payer': 'a', 'payer_id': 1, 'involved': ['a', 'b', 'c', 'd', 'e']},
    #     {'description': 'beer', 'amount': 10, 'payer': 'b', 'payer_id': 2, 'involved': ['a', 'b', 'c', 'd', 'e']},
    #     {'description': 'gas', 'amount': 30, 'payer': 'c', 'payer_id': 3, 'involved': ['a', 'b', 'c', 'd', 'e']},
    # ]
    # for payment in dummy_payments:
    #     dummy_payment = Payments(group_id='aaaaaa', description=payment['description'], amount=payment['amount'], payer=payment['payer'], payer_id=payment['payer_id'], involved=','.join(payment['involved']))
    #     db.session.add(dummy_payment)

    # new_group = Groups(group_id='bbbbbb')
    # db.session.add(new_group)
    # new_people = ['a', 'b']
    # for person in new_people:
    #     new_person = People(group_id='bbbbbb', name=person)
    #     db.session.add(new_person)
    # new_payments = [
    #     {'description': 'pizza', 'amount': 20, 'payer': 'a', 'payer_id': 1, 'involved': ['a', 'b']},
    # ]
    # for payment in new_payments:
    #     new_payment = Payments(group_id='bbbbbb', description=payment['description'], amount=payment['amount'], payer=payment['payer'], payer_id=payment['payer_id'], involved=','.join(payment['involved']))
    #     db.session.add(new_payment)

    # db.session.commit()
