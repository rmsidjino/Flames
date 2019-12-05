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

		'''
		{file:url_for(main.image', filename=file) for file in fs.list()}
		'''
		return redirect(url_for('.index'))
	return render_template('mypage.html',
							item_list = [i for i in db.get_collection('items').find()],
							file_lst = {file:url_for('main.image', filename=file) for file in fs.list()},
							form=form, name=session.get('name'),
							known=session.get('known', False),
							current_time=datetime.utcnow())

@mypage.route('/images/<filename>')
def image(filename):
    gridout = fs.get_last_version(filename=filename)
    return send_file(gridout, mimetype=gridout.content_type)