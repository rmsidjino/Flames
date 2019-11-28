
class User(object):
	username = ""
	ID = ""
	password = ""
	#permission = 0
	

	def __init__(self, username, ID, password, default=False):
		User.username = username
		User.ID = ID
		User.password = password
		#Flames.permission = permission
		User.default = default
				

	def to_dict(self):
		dict_flames = {
			'name': self.name, 
			'ID': self.ID,
			'passwd': self.password,
		#	'permission': self.permission,
			'default': self.default
		}
		return dict_flames

	def from_dict(self, data):
		if data is not None:
			self.name = data['name']
			self.ID = data['ID']
			self.password = data['password']
		#	self.permission = data['permission']
			self.default = data['default']

class Item(object):
	name = ""
	ID = ""
	price = ""
	picture = ""
	#permission = 0
	

	def __init__(self, name, ID, price, picture, default=False):
		Flames.name = name
		Flames.ID = ID
		Flames.price = price
		Flames.picture = picture
		#Flames.permission = permission
		Flames.default = default
				

	def to_dict(self):
		dict_flames = {
			'name': self.name, 
			'ID': self.ID,
			'price': self.price,
			'picture': self.picture,
		#	'permission': self.permission,
			'default': self.default
		}
		return dict_flames

	def from_dict(self, data):
		if data is not None:
			self.name = data['name']
			self.ID = data['ID']
			self.price = data['price']
			self.picture = data['picture']
		#	self.permission = data['permission']
			self.default = data['default']
			

