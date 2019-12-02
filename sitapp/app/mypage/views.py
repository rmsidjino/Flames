from datetime import datetime
from flask import render_template, session, redirect, url_for, flash,request

from . import mypage
from .forms import SearchitemForm

from ..models import User, Permission

from flask_login import login_user, login_required, logout_user
from ..decorators import admin_required, permission_required

# 20191122
from .. import db
from .forms import EditProfileForm, EditProfileAdminForm
from flask_login import current_user

from werkzeug import secure_filename
from .. import fs
from flask import send_file


@mypage.route('/', methods=['GET', 'POST'])
def index():
	return render_template('mypage.html',
							item_list = [i for i in db.get_collection('items').find()],
							file_lst = {file:url_for('main.image', filename=file) for file in fs.list()},
							name=session.get('name'),
							known=session.get('known', False),
							current_time=datetime.utcnow())
# 20191122


#@main.route('/search_hash')
#def search_hash(hid):
#     col_item = db.get_collection('hash_map')
#     results = col_item.find({'hid':hid})
#     return render_template('') ##


#def search(iid):
#     col_item = db.get_collection('item')
#     results = col_item.find({'hash_map':})
#     return render_template() ##


@mypage.route('/images/<filename>')
def image(filename):
    gridout = fs.get_last_version(filename=filename)
    return send_file(gridout, mimetype=gridout.content_type)