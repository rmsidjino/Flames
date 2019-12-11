from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Email, Length, Regexp, EqualTo

from wtforms import ValidationError
from ..models import Item
from .. import db

from wtforms import FileField

class RegistrationForm(FlaskForm):
   iname = StringField('iname', validators=[Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                     'inames must have only letters, '
                     'numbers, dots or underscores')])
   price = StringField('price', validators=[Required(), Length(1, 64)])
   req = StringField('How many sparks do you need?', validators=[Required(), Length(1, 64)])
   file = FileField('Upload an Image file', validators=[Required()])
   hash = StringField("Input hash tag!!(Insert a blank space each time you type a semicolon)",validators=[])
   submit = SubmitField('Register')