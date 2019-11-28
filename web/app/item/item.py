from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# 20191028
from . import login_manager, db

# 20191108
from flask import current_app, request, url_for
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer 
# 20191112
from flask_login import AnonymousUserMixin

# 20191122
from datetime import datetime

class Item(object):
	itemname = ""
	itemID = ""
	price = ""
	picture = ""
	#permission = 0
	

	def __init__(self, itemname, itemID, price, picture, default=False):
		Flames.itemname = itemname
		Flames.itemID = itemID
		Flames.price = price
		Flames.picture = picture
		#Flames.permission = permission
		Flames.default = default
				

	def to_dict(self):
		dict_flames = {
			'name': self.itemname, 
			'ID': self.itemID,
			'price': self.price,
			'picture': self.picture,
		#	'permission': self.permission,
			'default': self.default
		}
		return dict_flames

	def from_dict(self, data):
		if data is not None:
			self.itemname = data['itemname']
			self.itemID = data['itemID']
			self.price = data['price']
			self.picture = data['picture']
		#	self.permission = data['permission']
			self.default = data['default']
			
