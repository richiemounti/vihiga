from flask import (
    Blueprint,
    render_template,
    flash,
    g,
    session,
    redirect,
    url_for,
    request
)
from werkzeug.urls import url_parse
from flask_login import (
    login_user,
    logout_user,
    current_user
)
from app import db
from app.extensions import login
from app.models import User, Posts
from app.auth.forms import (
    LoginForm,
    RegistrationForm
)

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('post.index'))
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        remember_me = form.remember_me.data
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('post.index'))
        login_user(user, remember=remember_me)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('post.index')
        return redirect(next_page)
    
    return render_template('auth/login.html',
                            title='Login',
                            form=form
                            )

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('post.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('post.index'))
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    fullnames=form.fullnames.data,
                    phone_number=form.phone_number.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html',
                            title='Register',
                            form=form)