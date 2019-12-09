from datetime import datetime
from flask import render_template, session, redirect, url_for, flash,request

from . import mypage
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


@mypage.route('/', methods=['GET', 'POST'])
def index():
	form = SearchitemForm()
	if form.validate_on_submit():
		old_name = session.get('name')
		if old_name is not None and old_name != form.name.data:
			flash('Looks like you have changed your name!')
		session['name'] = form.name.data
		form.name.data = ''
		return redirect(url_for('.mypage'))
	current_time=datetime.now()
	try:
		collection = db.get_collection('users')
		results = collection.find({'id':current_user.id})
		collection = db.get_collection('items')
		collection.update_many({}, {'$set': {'participation': 'no'}})
		if results != None:
			collection.update_many({'participation_uid': current_user.id}, {'$set': {'participation': 'yes'}})
	except AttributeError:
		pass
	return render_template('mypage.html',
							item_list = [i for i in db.get_collection('items').find({'participation_uid':current_user.id})],
							file_lst = {file:url_for('main.image', filename=file) for file in fs.list()},
							form=form, name=session.get('name'),
							known=session.get('known', False),
							current_time=datetime.utcnow())

@mypage.route('/participation/<userid>/<iid>', methods=['GET'])
def participation(userid,iid):
	if current_user.is_authenticated:
		userid=current_user.id
		collection = db.get_collection('users')
		collection.update_one({'id':userid},{'$push':{'participation_iid':iid}})
		collection = db.get_collection('items')
		collection.update_one({'iid':iid},{'$push':{'participation_uid':userid}})
		result=[i for i in collection.find({'iid':iid})]
		num=str(len(result[0]['participation_uid']))
		collection.update_one({'iid':iid},{'$set':{'participation_num':num}})
		collection.update_one({'iid':iid},{'$set':{'participation':'yes'}})
		return redirect(url_for('.mypage'))
	else:
		flash("You must login!!")
		return render_template('need_login.html')

@mypage.route('/participation_out/<userid>/<iid>', methods=['GET'])
def participation_out(userid,iid):
	if current_user.is_authenticated:
		userid=current_user.id
		collection = db.get_collection('users')
		collection.update_one({'id':userid},{'$pull':{'participation_iid':iid}})
		collection = db.get_collection('items')
		collection.update_one({'iid':iid},{'$pull':{'participation_uid':userid}})
		result=[i for i in collection.find({'iid':iid})]
		num=str(len(result[0]['participation_uid']))
		collection.update_one({'iid':iid},{'$set':{'participation_num':num}})
		collection.update_one({'iid':iid},{'$set':{'participation':'no'}})
		return redirect(url_for('.mypage'))
	else:
		flash("You must login!!")
		return render_template('need_login.html')

@mypage.route('/images/<filename>')
def image(filename):
    gridout = fs.get_last_version(filename=filename)
    return send_file(gridout, mimetype=gridout.content_type)