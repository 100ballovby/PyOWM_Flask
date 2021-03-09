from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm


class SearchForm(FlaskForm):
    city = StringField('City name')
    submit = SubmitField('Submit')