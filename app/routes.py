from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm,delete
from app.models import User
import json

@app.context_processor
def inject_user():

    user_c=current_user.username
    return dict(user_c=user_c)

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():   
    return render_template('index.html', title='Home')


@app.route('/LoginPanel', methods=['GET', 'POST'])
def login():
    current_user.username=""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('loginPanel.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user/',methods=['GET', 'POST'])
@login_required
def user():
    form = RegistrationForm()
    form2 =delete()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, surrname=form.surrname.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('index.html'))
    if form2.validate_on_submit():
       option = request.form['id']
       obj = User.query.filter_by(id=option).one()
       db.session.delete(obj)
       db.session.commit()
       return redirect(url_for('index'))

    return render_template('listOfPeople.html', users = User.query.all(),title='Register', form=form)



@app.route('/yourStats/',methods=['GET', 'POST'])
@login_required
def yourStats():
    legend = 'Monthly Data'
    dniLiniowy = ["January", "February", "March", "April", "May", "June", "July", "August"]
    iloscLiniowy = [10, 9, 8, 7, 6, 4, 7, 18]
    procentWoda=60
    procentCena=70
    procentIlosc=80
    procentLitry=90

    return render_template('profile.html', values=iloscLiniowy, labels=dniLiniowy,procentWoda=procentWoda,procentIlosc=procentIlosc,procentLitry=procentLitry,procentCena=procentCena)


@app.route('/allData/',methods=['GET', 'POST'])
@login_required
def allData():
    result ="result"

    osoby=[]
    for id in User.query.all():
        osoby.append(id.username)
    legend = 'Monthly Data'
    iloscLitrow = [10, 20, 50, 20]
    return render_template('charts.html',osoby=osoby)

