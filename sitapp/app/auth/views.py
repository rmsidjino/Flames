from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user
from ..models import User
from .forms import LoginForm, RegistrationForm
from . import auth

from .. import db
from ..email import send_email 

from flask_login import current_user

@auth.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		collection = db.get_collection('users')
		results = collection.find_one({'id':form.email.data})
		if results is not None:
			user = User(form.email.data, "", "") 
			user.from_dict(results)
			if user is not None and user.verify_password(form.password.data):
				login_user(user, form.remember_me.data)
				return redirect(request.args.get('next') or url_for('main.index'))
		flash('Invalid username or password.')
	return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have been logged out.')
	collection = db.get_collection('items')
	collection.update_many({}, {'$set': {'participation': 'no'}})
	return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register(): 
    form = RegistrationForm() 
    if form.validate_on_submit(): 
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        collection = db.get_collection('users')
        collection.insert_one(user.to_dict())        
        token = user.generate_confirmation_token()
        send_email(user.id, 'Confirm Your Account', 'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)

@auth.route('/confirm/<token>') 
@login_required 
def confirm(token): 
    if current_user.confirmed: 
        return redirect(url_for('main.index')) 
    if current_user.confirm(token): 
        flash('You have confirmed your account. Thanks!') 
    else: 
        flash('The confirmation link is invalid or has expired.') 
    return redirect(url_for('main.index'))

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed and request.endpoint[:5] != 'auth.':
            return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
	if current_user.is_anonymous or current_user.confirmed:
		return redirect('main.index')
	return render_template('auth/unconfirmed.html')

@auth.route('/confirm')
@login_required
def resend_confirmation():
	token = current_user.generate_confirmation_token()
	send_email(current_user.id,'Confirm Your Account','auth/email/confirm.html', user=current_user, token=token)
	flash('A new confirmation email has been sent to you by email.')
	return redirect(url_for('main.index'))
