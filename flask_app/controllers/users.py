from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard')
def welcome():
    return render_template('dashboard.html', all_users=User.get_all())

@app.route('/register', methods=['POST'])
def register():
    isValid = User.validate(request.form)
    if not isValid:
        # we redirect to the template with the form
        return redirect('/')

    data = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password" : bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    print(data)
    # do other things
    if not id: 
        flash('Something went wrong!')
        return redirect('/')
    session['user_id'] = id
    session['first_name'] = request.form['first_name']
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    data = {"email" : request.form['email']}
    user_in_db = User.get_by_email(data) 
    
    # do other things
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect('/')

    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect("/dashboard")
    # This is add a user in session
    session['user_id'] = user_in_db.id
    session['first_name'] = user_in_db.first_name
    return redirect('/dashboard')






@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id' : session['user_id']
    }
    return render_template("dashboard.html", user=User.get_by_id(data))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
