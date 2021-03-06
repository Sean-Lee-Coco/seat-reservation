from gmdp import app,db
from flask import render_template, redirect, request, url_for, flash, abort
from flask_login import login_user,login_required,logout_user,current_user
from gmdp.models import User
from gmdp.forms import LoginForm, RegistrationForm
from werkzeug.security import generate_password_hash, check_password_hash
import datetime as dt

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/seat_reservation')
@login_required
def seat_reservation():
    return render_template('seat_reservation.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You logged out!')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    # Create instance of the form.
    form = LoginForm()
    # If the form is valid on submission
    if form.validate_on_submit():
        # Grab the data from the breed on the form.
        user = User.query.filter_by(email=form.email.data).first()
        #session['id'] = form.id.data
        #session['pwd'] = form.pwd.data

        if user is not None and user.check_password(form.password.data):
            #Log in the user

            login_user(user)

            flash('Logged in successfully.')

            next = request.args.get('next')

            if next == None or not next[0]=='/':
                next = url_for('seat_reservation')

            return redirect(next)
        else:
            flash('Invalid Username or Password')

    return render_template('login.html', form=form)

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    # Create instance of the form.
    form = RegistrationForm()
    # If the form is valid on submission

    if form.validate_on_submit():
        # Grab the data from the breed on the form.
        user = User(#type=form.type.data,
                    email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering! Now you can login!')

        return redirect(url_for('login'))
    return render_template('sign_up.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
