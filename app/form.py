from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

class SearchForm(FlaskForm):
    stadName = StringField('stadName', validators = [DataRequired(), Length(min = 0, max = 100)])

class SignupForm(FlaskForm):
    signName = StringField('signName', validators = [DataRequired(), Length(min = 0, max = 100)])
    signPassword = StringField('signPassword', validators = [DataRequired(), Length(min = 0, max = 100)])

class LoginForm(FlaskForm):
    loginName = StringField('loginName', validators = [DataRequired(), Length(min = 0, max = 100)], render_kw={"placeholder": "UserName"})
    loginPassword = StringField('loginPassword', validators = [DataRequired(), Length(min = 0, max = 100)], render_kw={"placeholder": "Password"})