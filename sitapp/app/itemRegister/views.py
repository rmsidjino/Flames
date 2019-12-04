from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user
from ..models import Item
from .forms import RegistrationForm
from . import itemRegister

from .. import db

from werkzeug import secure_filename
from .. import fs
from flask import send_file

@itemRegister.route('/', methods=['GET', 'POST'])
def register(): 
    form = RegistrationForm() 
    if form.validate_on_submit(): 
        filename = secure_filename(form.file.data.filename)
        oid = fs.put(form.file.data, content_type=form.file.data.content_type, filename=filename)
        item = Item(iid=form.iid.data, iname=form.iname.data, price=form.price.data, req=form.req.data, dday=form.dday.data, file=filename, hash_data=form.hash.data.split())
        collection = db.get_collection('items')
        collection.insert_one(item.to_dict())
        return redirect(url_for('main.index'))
    return render_template('itemRegister/register.html', form=form)


@itemRegister.route('/images/<filename>')
def image(filename):
    gridout = fs.get_last_version(filename=filename)
    return send_file(gridout, mimetype=gridout.content_type)