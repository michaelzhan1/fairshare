from flask import Flask
from calculate import calculate_debts
from flask import render_template, redirect, request, jsonify
from random import choice
import string
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://default:J8ZgCxfYB9bO@ep-divine-boat-313077.us-east-1.postgres.vercel-storage.com:5432/verceldb"
# app.config['FLASK_ENV'] = 'production'


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
    db.create_all()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/new_group')
def new_group():
    all_groups = db.session.query(Groups.group_id).distinct().all()
    all_groups = [g[0] for g in all_groups]
    new_group = ''.join(choice(string.ascii_lowercase) for i in range(6))
    while new_group in all_groups:
        new_group = ''.join(choice(string.ascii_lowercase) for i in range(6))
    group = Groups(group_id=new_group)
    db.session.add(group)
    db.session.commit()
    return redirect(f'/g/{new_group}')


@app.route('/g/<group>', methods=['GET', 'POST'])
def group_page(group):
    all_groups = db.session.query(Groups.group_id).distinct().all()
    all_groups = [g[0] for g in all_groups]
    if group not in all_groups:
        return redirect('/')
    return render_template('group.html', groupid=group)


@app.route('/api/add_person', methods=['POST'])
def add_person():
    if request.method == 'POST':
        groupid = request.form['groupid']
        all_groups = db.session.query(Groups.group_id).distinct().all()
        all_groups = [g[0] for g in all_groups]
        if groupid not in all_groups:
            return redirect('/')
        name = request.form['name']
        person = People(name=name, group_id=groupid)
        db.session.add(person)
        db.session.commit()
        return redirect(f'/g/{groupid}')
    return redirect('/')


@app.route('/api/add_payment', methods=['POST'])
def add_payment():
    if request.method == 'POST':
        groupid = request.form['groupid']
        all_groups = db.session.query(Groups.group_id).distinct().all()
        all_groups = [g[0] for g in all_groups]
        if groupid not in all_groups:
            return redirect('/')
        description = request.form['description']
        amount = float(request.form['amount'])
        payer = request.form['payer']
        involved = request.form.getlist('involved')
        involved_string = ','.join(involved)
        payer_id = db.session.query(People.id).filter_by(name=payer).first()[0]
        payment = Payments(group_id=groupid, description=description, amount=amount, payer=payer, payer_id=payer_id, involved=involved_string)
        db.session.add(payment)
        db.session.commit()        
        return redirect(f'/g/{groupid}')
    return redirect('/')


@app.route('/api/edit_payment', methods=['POST'])
def edit_payment():
    if request.method == 'POST':
        data = request.get_json()
        payment_data = data['payment']
        description = payment_data['description']
        amount = float(payment_data['amount'])
        payer = payment_data['payer']
        involved_string = ','.join(payment_data['involved'])

        groupid = data['groupid']

        payment_id = data['paymentid']
        payment = Payments.query.filter_by(id=payment_id).first()
        payment.description = description
        payment.amount = amount
        payment.payer = payer
        payment.involved = involved_string
        db.session.commit()
        return redirect(f'/g/{groupid}')
    return redirect('/')


@app.route('/api/delete_payment', methods=['POST'])
def delete_payment():
    if request.method == 'POST':
        data = request.get_json()
        payment_id = data['paymentid']
        payment = Payments.query.filter_by(id=payment_id).first()
        db.session.delete(payment)
        db.session.commit()
        groupid = data['groupid']
        return redirect(f'/g/{groupid}')
    return redirect('/')



@app.route('/api/get_people', methods=['POST'])
def get_people():
    data = request.get_json()
    groupid = data['groupid']
    all_groups = db.session.query(Groups.group_id).distinct().all()
    all_groups = [g[0] for g in all_groups]
    if groupid not in all_groups:
        return redirect('/')

    people = db.session.query(People.name).filter_by(group_id=groupid).all()
    return jsonify(names=[p[0] for p in people])


@app.route('/api/get_payments', methods=['POST'])
def get_payments():
    data = request.get_json()
    groupid = data['groupid']
    all_groups = db.session.query(Groups.group_id).distinct().all()
    all_groups = [g[0] for g in all_groups]
    if groupid not in all_groups:
        return redirect('/')
    
    payments = db.session.query(Payments.amount, Payments.payer, Payments.involved, Payments.date, Payments.description, Payments.id).filter_by(group_id=groupid).all()
    return jsonify(payments=[{'amount': p[0], 'payer': p[1], 'involved': p[2], 'date': p[3], 'description': p[4], 'id': p[5]} for p in payments])


@app.route('/api/get_single_payment', methods=['POST'])
def get_single_payment():
    data = request.get_json()
    payment_id = data['paymentid']
    payment = db.session.query(Payments.amount, Payments.payer, Payments.involved, Payments.date, Payments.description, Payments.id).filter_by(id=payment_id).first()
    return jsonify(payment={'amount': payment[0], 'payer': payment[1], 'involved': payment[2].split(','), 'date': payment[3], 'description': payment[4], 'id': payment[5]})


@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    groupid = data['groupid']
    all_groups = db.session.query(Groups.group_id).distinct().all()
    all_groups = [g[0] for g in all_groups]
    if groupid not in all_groups:
        return redirect('/')
    raw_people = db.session.query(People.name).filter_by(group_id=groupid).all()
    people = [p[0] for p in raw_people]

    raw_payment_info = db.session.query(Payments.amount, Payments.payer, Payments.involved).filter_by(group_id=groupid).all()
    payment_info = list(zip(*raw_payment_info))
    payment_info[2] = tuple(map(lambda x: x.split(','), payment_info[2]))
    debts = calculate_debts(people, *payment_info)
    return jsonify(debts=debts)