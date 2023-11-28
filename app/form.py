from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, DateField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import TextArea

class SearchForm(FlaskForm):
    stadName = StringField('stadName', validators = [DataRequired(), Length(min = 0, max = 100)])

class SignupForm(FlaskForm):
    signUsername = StringField('signUsername', validators = [DataRequired(), Length(min = 0, max = 100)], render_kw={"placeholder": "Username"})
    signPassword = StringField('signPassword', validators = [DataRequired(), Length(min = 0, max = 100)], render_kw={"placeholder": "Password"})
    signName = StringField('signName', validators = [DataRequired(), Length(min = 0, max = 100)], render_kw={"placeholder": "Enter your Name"})

class LoginForm(FlaskForm):
    loginName = StringField('loginName', validators = [DataRequired(), Length(min = 0, max = 100)], render_kw={"placeholder": "Username"})
    loginPassword = StringField('loginPassword', validators = [DataRequired(), Length(min = 0, max = 100)], render_kw={"placeholder": "Password"})

class ReviewForm(FlaskForm):
    stadName = StringField('stadName', validators = [DataRequired()])
    rating = RadioField('rating', choices=[('1','☆'),('2','☆'),('3','☆'),('4','☆'),('5','☆')])
    title = StringField('title', validators = [DataRequired(), Length(min = 0, max = 100)], render_kw={"placeholder": "Title of Review"})
    date = DateField('date', validators = [DataRequired()])
    reviewText = StringField('reviewText',  validators = [DataRequired()], widget = TextArea(), render_kw={"placeholder": "Tell us about your visit"})