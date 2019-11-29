from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user
from ..models import User

from .. import db
from ..email import send_email # added 20191108

from flask_login import current_user

## 20191129
from .forms import ImageRegisterForm
from . import img

from werkzeug import secure_filename
from .. import fs
from flask import send_file

@img.route('/', methods=['GET', 'POST'])
def show_images():
	return render_template('img/img_lst.html', 
		file_lst = [url_for('img.image', filename=file) for file in fs.list()])

@img.route('/register', methods=['GET', 'POST'])
def register_images():
    form = ImageRegisterForm()
    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        oid = fs.put(form.file.data, content_type=form.file.data.content_type, filename=filename)
        print(filename)
        return redirect(url_for('img.show_images'))
    return render_template('img/img_register.html', form=form)


@img.route('/images/<filename>')
def image(filename):
    gridout = fs.get_last_version(filename=filename)
    return send_file(gridout, mimetype=gridout.content_type)