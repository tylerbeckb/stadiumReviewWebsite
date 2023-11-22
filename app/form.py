from flask_wtf import FlaskForm
from wtforms import StringField, default
from wtforms.validators import DataRequired, Length, default

class SearchForm(FlaskForm):
    stadName = StringField('stadName', validators = [DataRequired(), Length(min = 0, max = 100), default='Enter Stadium'])