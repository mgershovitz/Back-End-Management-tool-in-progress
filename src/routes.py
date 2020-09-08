from functools import wraps

from flask import render_template, flash, url_for, session
from werkzeug.utils import redirect

from src.DB.Models.DTO.user import User
from src.run import app
from src.forms import LoginForm, RegisterNurseForm, InsertNewBirthData
from session_utils import loginUser


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap


# dummy data
posts = [
        {
            'nurse_name': 'Nurit Lev',
            'role': 'Nurse',
            'work_years': '14',
            'employment_percentage': '100%'
        },
        {
            'nurse_name': 'Tali Queen',
            'role': 'Nurse',
            'work_years': '35',
            'employment_percentage': '100%'
        },
    ]


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/nurse/screen")
@login_required
def nurse_screen():
    return render_template('nurse_screen.html', posts=posts)


@app.route("/cs_prediction",  methods=['GET', 'POST'])
@login_required
def cs_prediction():
    form = InsertNewBirthData()
    if form.validate_on_submit():
        return render_template('cs_prediction.html', title='Cs_prediction', form=form) #TODO: fix it
    else:
        return "in progress"


@app.route("/department")
@login_required
def department():
    return render_template('department.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = NurseUser.get_nurse(form.email.data)
        if user.validate_password(form.password.data):
            loginUser(user)
            flash('You have been logged in!', 'success')
            return redirect(url_for('nurse'))
        else:
             flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    return User().logout()


@app.route("/register/nurse", methods=['GET', 'POST'])
@login_required
def register_nurse():
    form = RegisterNurseForm()
    if form.validate_on_submit():
        return User().register_nurse()
    #     flash('You have been Register a Nurse!', 'success')
    # else:
    #    flash('Register Unsuccessful. Please check username and password', 'danger')
    return render_template('register_nurse.html', title='register_nurse', form=form)
