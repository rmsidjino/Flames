from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import Required, Email, Length

from wtforms import SelectField, ValidationError
from wtforms.validators import Regexp, EqualTo
from .. import db


class SearchitemForm(FlaskForm):    
    name = StringField('What item are you interested in?', validators=[Required()])    
    submit = SubmitField('Search') 

class EditProfileForm(FlaskForm):
	username = StringField('Real name', validators=[Length(0, 64)])
	submit = SubmitField('Submit')

class EditProfileAdminForm(FlaskForm):
	id = StringField('Email', validators=[Required(), Length(1, 64), Email()])
	username = StringField('Username', validators=[Required(), Length(1, 64), 
		Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Usernames must have only letters, ''numbers, dots or underscores')])
	confirmed = BooleanField('Confirmed')
	role = SelectField('Role')
	username = StringField('Real name', validators=[Length(0, 64)])
	submit = SubmitField('Submit')

	def __init__(self, user, *args, **kwargs):
		super(EditProfileAdminForm, self).__init__(*args, **kwargs)
		collection = db.get_collection('roles')
		results = collection.find({ } , { "name": True })
		
		lst = [result['name'] for result in results] 
		r_lst = [(role, role) for role in lst]

		self.role.choices = r_lst
		self.user = user

	def validate_email(self, field):
		collection = db.get_collection('users')
		results = collection.find_one({'id':field.data})
		if results is not None:
			raise ValidationError('Email already registered.')
		pass

class RegisterItemAdminForm(FlaskForm):
	iid = StringField('iname', validators=[Length(0, 64)])
	username = StringField('Username', validators=[Required(), Length(1, 64), 
		Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Usernames must have only letters, ''numbers, dots or underscores')])
	confirmed = BooleanField('Confirmed')
	role = SelectField('Role')
	username = StringField('Real name', validators=[Length(0, 64)])
	submit = SubmitField('Submit')

	def __init__(self, user, *args, **kwargs):
		super(EditProfileAdminForm, self).__init__(*args, **kwargs)
		collection = db.get_collection('roles')
		results = collection.find({ } , { "name": True })
		
		lst = [result['name'] for result in results] 
		r_lst = [(role, role) for role in lst]

		self.role.choices = r_lst
		self.user = user

	def validate_email(self, field):
		collection = db.get_collection('users')
		results = collection.find_one({'id':field.data})
		if results is not None:
			raise ValidationError('Email already registered.')
		pass