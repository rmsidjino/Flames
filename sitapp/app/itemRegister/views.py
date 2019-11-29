from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user
from ..models import Item
from .forms import RegistrationForm
from . import itemRegister

from .. import db



@itemRegister.route('/', methods=['GET', 'POST'])
def register(): 
    form = RegistrationForm() 
    if form.validate_on_submit(): 
        item = Item(iid=form.iid.data, iname=form.iname.data, price=form.price.data, req=form.req.data)
        collection = db.get_collection('items')
        collection.insert_one(item.to_dict())
        return redirect(url_for('main.index'))
        #return redirect(url_for('itemRegister.login')) 
        ###
    return render_template('itemRegister/register.html', form=form)

 