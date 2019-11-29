from flask import Blueprint

itemRegister = Blueprint('itemRegister', __name__)

from . import views
