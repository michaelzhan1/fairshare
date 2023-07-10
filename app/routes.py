from app import app
from app.models import People, Payments, db
from app.calculate import calculate_debts
from flask import render_template, redirect, request, jsonify


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/add_person', methods=['POST'])
def add_person():
    if request.method == 'POST':
        name = request.form['name']
        person = People(name=name)
        db.session.add(person)
        db.session.commit()
    return redirect('/')


@app.route('/add_payment', methods=['POST'])
def add_payment():
    if request.method == 'POST':
        description = request.form['description']
        amount = float(request.form['amount'])
        payer = request.form['payer']
        involved = request.form.getlist('involved')
        involved_string = ','.join(involved)
        payer_id = db.session.query(People.id).filter_by(name=payer).first()[0]
        payment = Payments(description=description, amount=amount, payer=payer, payer_id=payer_id, involved=involved_string)
        db.session.add(payment)
        db.session.commit()        
    return redirect('/')


@app.route('/edit_payment', methods=['POST'])
def edit_payment():
    if request.method == 'POST':
        data = request.get_json()
        payment_data = data['payment']
        description = payment_data['description']
        amount = float(payment_data['amount'])
        payer = payment_data['payer']
        involved_string = ','.join(payment_data['involved'])

        print(data)
        payment_id = data['paymentid']
        payment = Payments.query.filter_by(id=payment_id).first()
        payment.description = description
        payment.amount = amount
        payment.payer = payer
        payment.involved = involved_string
        db.session.commit()
    return redirect('/')


@app.route('/delete_payment', methods=['POST'])
def delete_payment():
    if request.method == 'POST':
        data = request.get_json()
        payment_id = data['paymentid']
        payment = Payments.query.filter_by(id=payment_id).first()
        db.session.delete(payment)
        db.session.commit()
    return redirect('/')



@app.route('/get_people', methods=['POST'])
def get_people():
    people = db.session.query(People.name).all()
    return jsonify(names=[p[0] for p in people])


@app.route('/get_payments', methods=['POST'])
def get_payments():
    payments = db.session.query(Payments.amount, Payments.payer, Payments.involved, Payments.date, Payments.description, Payments.id).all()
    return jsonify(payments=[{'amount': p[0], 'payer': p[1], 'involved': p[2], 'date': p[3], 'description': p[4], 'id': p[5]} for p in payments])


@app.route('/get_single_payment', methods=['POST'])
def get_single_payment():
    data = request.get_json()
    print(data)
    payment_id = data['paymentid']
    payment = db.session.query(Payments.amount, Payments.payer, Payments.involved, Payments.date, Payments.description, Payments.id).filter_by(id=payment_id).first()
    return jsonify(payment={'amount': payment[0], 'payer': payment[1], 'involved': payment[2].split(','), 'date': payment[3], 'description': payment[4], 'id': payment[5]})


@app.route('/calculate', methods=['POST'])
def calculate():
    raw_people = db.session.query(People.name).all()
    people = [p[0] for p in raw_people]

    raw_payment_info = db.session.query(Payments.amount, Payments.payer, Payments.involved).all()
    payment_info = list(zip(*raw_payment_info))
    payment_info[2] = tuple(map(lambda x: x.split(','), payment_info[2]))
    debts = calculate_debts(people, *payment_info)
    return jsonify(debts=debts)