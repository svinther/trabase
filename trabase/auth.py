from flask_login import login_required, logout_user, current_user, login_user, UserMixin

#this file must be imported within the "with app_context()" context
from flask import current_app as app, flash, request, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Length, Email, DataRequired
from werkzeug.security import generate_password_hash, check_password_hash

from . import login_manager
from . import db

class User(UserMixin, db.Model):
    """Model for user accounts."""

    __tablename__ = 'user'

    id = db.Column(db.Integer,
                   primary_key=True)
    name = db.Column(db.String,
                     nullable=False,
                     unique=False)
    email = db.Column(db.String(40),
                      unique=True,
                      nullable=False)
    password = db.Column(db.String(200),
                         primary_key=False,
                         unique=False,
                         nullable=False)
    created_on = db.Column(db.DateTime,
                           index=False,
                           unique=False,
                           nullable=True)
    last_login = db.Column(db.DateTime,
                           index=False,
                           unique=False,
                           nullable=True)

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)



class LoginForm(FlaskForm):
    email = StringField('Email',validators=[Email(message=('Please enter a valid email address.')),
                                    DataRequired(message=('Please enter a valid email address.'))])
    password = PasswordField('Password', validators=[DataRequired("Please enter password")])


@login_manager.user_loader
def user_loader(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    logout_user()
    return 'Logged out'


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template('login.html', form=LoginForm())

    # POST request
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    login_form = LoginForm(request.form)
    if login_form.validate():
        # Get Form Fields
        email = request.form.get('email')
        password = request.form.get('password')
        # Validate Login Attempt
        user = User.query.filter_by(email=email).first()
        if user:
            if user.check_password(password=password):
                login_user(user)
                return redirect(url_for('main'))
        flash('Invalid username/password combination')
    return redirect(url_for('login'))


def create_admin_user():
    admin_user = User.query.filter_by