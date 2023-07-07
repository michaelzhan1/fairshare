from app import app
from app.models import People, Payments, db
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


@app.route('/get_people', methods=['GET'])
def get_people():
    people = db.session.query(People.name).all()
    return jsonify(names=[p[0] for p in people])