from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, DateField, PasswordField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import TextArea

# Used to search a stadiums reviews
class SearchForm(FlaskForm):
    stadName = StringField('stadName', validators = [DataRequired(), Length(min = 0, max = 100)])

# Used to sign up new users
class SignupForm(FlaskForm):
    signUsername = StringField('signUsername', validators = [DataRequired(), Length(min = 0, max = 100)],
                        render_kw={"placeholder": "Username"})
    signPassword = PasswordField('signPassword', validators = [DataRequired(), Length(min = 0, max = 100)],
                        render_kw={"placeholder": "Password"})
    signName = StringField('signName', validators = [DataRequired(), Length(min = 0, max = 100)],
                        render_kw={"placeholder": "Enter your Name"})

# Used to login users
class LoginForm(FlaskForm):
    loginName = StringField('loginName', validators = [DataRequired(), Length(min = 0, max = 100)],
                        render_kw={"placeholder": "Username"})
    loginPassword = PasswordField('loginPassword', validators = [DataRequired(), Length(min = 0, max = 100)],
                        render_kw={"placeholder": "Password"})

# Uaed to write a review
class ReviewForm(FlaskForm):
    rating = RadioField('rating', choices=[('1','☆'),('2','☆'),('3','☆'),('4','☆'),('5','☆')],
                        validators = [DataRequired()])
    title = StringField('title', validators = [DataRequired(), Length(min = 0, max = 100)],
                        render_kw={"placeholder": "Title of Review"})
    date = DateField('date', validators = [DataRequired()])
    reviewText = StringField('reviewText',  validators = [DataRequired()], widget = TextArea(),
                        render_kw={"placeholder": "Tell us about your visit"})

# Used for users to edit their name
class EditName(FlaskForm):
    newName = StringField('newName', validators = [DataRequired(), Length(min = 0, max = 100)],
                        render_kw={"placeholder": "Enter your new Name"})
    sameName = StringField('sameName', validators = [DataRequired(), Length(min = 0, max = 100)],
                        render_kw={"placeholder": "Enter your Name again"})