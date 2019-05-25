from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField
)
from wtforms.validators import (
    DataRequired,
    EqualTo
)
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
            initial_validation = super(LoginForm, self).validate()
            if not initial_validation:
                return False

            self.user = User.query.filter_by(username=self.username.data).first()
            if not self.user:
                self.username.errors.append('Username not found')
                return False

            if not self.user.check_password(self.password.data):
                self.password.errors.append('Invalid password')
                return False

            return True
    
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    fullnames = StringField('Full Name', validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Verify Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.user = None
    
    def validate(self):
        initial_validation = super(RegistrationForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append('Username already registered')
            return False
        
        user = User.query.filter_by(phone_number=self.phone_number.data).first()
        if user:
            self.phone_number.errors.append('Phonenumber already registered')
            return False
        
        return True
