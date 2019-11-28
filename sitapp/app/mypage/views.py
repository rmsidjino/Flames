from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user
from ..models import User
from .forms import LoginForm, RegistrationForm
from . import mypage

from .. import db
from ..email import send_email # added 20191108

from flask_login import current_user

@mypage.route('/', methods=['GET', 'POST'])
def mypage_main():
    return "My Page"
