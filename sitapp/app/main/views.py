from datetime import datetime
from flask import render_template, session, redirect, url_for, flash,request

from . import main
from .forms import SearchitemForm
from ..models import User, Permission

from flask_login import login_user, login_required, logout_user
from ..decorators import admin_required, permission_required

from .. import db
from .forms import EditProfileForm, EditProfileAdminForm
from flask_login import current_user

from werkzeug import secure_filename
from .. import fs
from flask import send_file
from bson.objectid import ObjectId

from datetime import datetime
from dateutil.relativedelta import *

@main.route('/', methods=['GET', 'POST'])
def index():
	form = SearchitemForm()
	if form.validate_on_submit():
		old_name = session.get('name')
		if old_name is not None and old_name != form.name.data:
			flash('Looks like you have changed your name!')
		session['name'] = form.name.data
		form.name.data = ''

		'''
		{file:url_for(main.image', filename=file) for file in fs.list()}
		'''
		return redirect(url_for('.index'))
	current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	try:
		collection = db.get_collection('users')
		results = collection.find({'id':current_user.id})
		collection = db.get_collection('items')
		collection.update_many({}, {'$set': {'participation': 'no'}})
		if results != None:
			collection.update_many({'participation_uid': current_user.id}, {'$set': {'participation': 'yes'}})
	except AttributeError:
		pass
	return render_template('index.html',
							item_list = [i for i in db.get_collection('items').find()],
							file_lst = {file:url_for('main.image', filename=file) for file in fs.list()},
							form=form, name=session.get('name'),
							known=session.get('known', False),
							current_time=current_time)

@main.route('/user/<username>')
def user(username):
	collection = db.get_collection('users')
	results = collection.find_one({'username':username})
	if results is not None:
		user = User("", "", "") 
		user.from_dict(results)
		return render_template('user.html', user=user)
	else:
		abort(404)

@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	form = EditProfileForm()
	if form.validate_on_submit():
		current_user.username = form.username.data	
		
		# db update
		collection = db.get_collection('users')
		collection.delete_one({'id':current_user.id})
		collection.insert_one(current_user.to_dict())

		flash('Your profile has been updated.')
		return redirect(url_for('.user', username=current_user.username))
	form.username.data = current_user.username
	return render_template('edit_profile.html', form=form)

@main.route('/edit-profile/<id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
	collection = db.get_collection('users')
	result = collection.find_one({'id':id})
	if result != None:
		user = User(id, "", "")
		user.from_dict(result)
		form = EditProfileAdminForm(user=user)
		if form.validate_on_submit():
			user.id = form.id.data
			user.username = form.username.data
			user.confirmed = form.confirmed.data
			# db update
			collection = db.get_collection('users')
			collection.update_one({'id':user.id}, {'$set':{'role_id':form.role.data}})
			
			flash('The profile has been updated.')
			return redirect(url_for('.user', username=user.username))
		form.id.data = user.id
		form.username.data = user.username
		form.confirmed.data = user.confirmed
		form.role.data = user.role.name
		return render_template('edit_profile.html', form=form, user=user)
	else:
		abort(404)

@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return "For administrators!"

@main.route('/moderator')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def for_moderators_only():
    return "For comment moderators!"

@main.route('/search/<item>', methods=['GET', 'POST'])
def search(item):
	form = SearchitemForm()
	if form.validate_on_submit():
		old_name = session.get('name')
		if old_name is not None and old_name != form.name.data:
			flash('Looks like you have changed your name!')
		session['name'] = form.name.data
		form.name.data = ''
		return redirect(url_for('.index'))
	current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	return render_template('index.html',
							item_list = [i for i in db.get_collection('items').find({'hash_data':item})],
							file_lst = {file:url_for('main.image', filename=file) for file in fs.list()},
							form=form, name=session.get('name'),
							known=session.get('known', False),
							current_time=current_time)

#<<<<<<< HEAD
@main.route('/participation/<userid>/<iid>', methods=['GET'])
def participation(userid,iid):
	if current_user.is_authenticated:
		userid=current_user.id
		collection = db.get_collection('items')
		collection.update_one({'_id':ObjectId(iid)},{'$push':{'participation_uid':userid}})
		result=[i for i in collection.find({'_id':ObjectId(iid)})]
		num=str(len(result[0]['participation_uid']))
		collection.update_one({'_id':ObjectId(iid)},{'$set':{'participation_num':num}})
		return redirect(url_for('.index'))
	else:
		flash("You must login!!")
		return render_template('need_login.html')

@main.route('/participation_out/<userid>/<iid>', methods=['GET'])
def participation_out(userid,iid):
	if current_user.is_authenticated:
		userid=current_user.id
		collection = db.get_collection('items')
		collection.update_one({'_id':ObjectId(iid)},{'$pull':{'participation_uid':userid}})
		result=[i for i in collection.find({'_id':ObjectId(iid)})]
		num=str(len(result[0]['participation_uid']))
		collection.update_one({'_id':ObjectId(iid)},{'$set':{'participation_num':num}})
		return redirect(url_for('.index'))
	else:
		flash("You must login!!")
		return render_template('need_login.html')


@main.route('/images/<filename>')
def image(filename):
    gridout = fs.get_last_version(filename=filename)
    return send_file(gridout, mimetype=gridout.content_type)