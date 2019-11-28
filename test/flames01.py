class User(UserMixin, object):
	id = ""
	username = "cbchoi"
	role = None 
	password_hash = ""
	confirmed = False
	member_since = ""
	last_seen = ""

	def __init__(self, id, username, password):
		self.id = email
		self.username = username
		self.password = password

		collection = db.get_collection('roles')
		if self.id == current_app.config['ADMIN']:
			self.role = Role('Administrator', 0xff)
		else:
			result = collection.find_one({'default':True})
			self.role = Role(result['name'], result['permission'], result['default'])
		 
	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')
	 
	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)
	
	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	@login_manager.user_loader
	def load_user(user_id):
		collection = db.get_collection('users')
		results = collection.find_one({'id':user_id})
		if results is not None:
			user = User(results['id'], "", "") # 20191112
			user.from_dict(results)
			return user
		else:
			return None

	def generate_confirmation_token(self, expiration=3600):
		s = Serializer(current_app.config['SECRET_KEY'], expiration)
		return s.dumps({'confirm': self.id}).decode('utf-8')

	def confirm(self, token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token.encode('utf-8'))
		except:
			return False
		if data.get('confirm') != self.id:
			return False
		self.confirmed = True
		collection = db.get_collection('users')
		results = collection.update_one({'id':self.id}, {'$set':{'confirmed':self.confirmed}})
		return True

	def can(self, permissions):
		return self.role is not None and (self.role.permission & permissions) == permissions
    
	def is_administrator(self):
		return self.can(Permission.ADMINISTATOR)

	def ping(self):
		self.last_seen = datetime.utcnow()
		collection = db.get_collection('users')
		results = collection.update_one({'id':self.id}, {'$set':{'last_seen':self.last_seen}})

	def to_dict(self):
		dict_user = {
			'id': self.id, 
			'username':self.username,

			'role_id':self.role.name,
			'role_permission':self.role.permission,

			'password_hash':self.password_hash,
			'confirmed':self.confirmed,

			'member_since':self.member_since,
			'last_seen':self.last_seen
		}
		return dict_user

	def from_dict(self, data):
		if data is not None:
			self.id = data['id']
			self.username = data['username']

			self.role = Role(data['role_id'], data['role_permission'])

			self.password_hash = data['password_hash']
			self.confirmed = data['confirmed']

			self.member_since = data.get('member_since')
			self.last_seen = data.get('last_seen')


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
			

