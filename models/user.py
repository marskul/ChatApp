from db import db

class UserModel(db.Model):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80))
	email = db.Column(db.String(80))
	password = db.Column(db.String(80))
	friends = db.Column(db.Integer)

	def __init__(self, username, email, password):
		self.username = username
		self.email = email
		self.password = password
		self.friends = 0

	def jsonify(self):
		return{'user': self.username, 'email': self.email, 'id': self.id}

	def check_data(self):
		if self.username and self.password and self.email:
			return True
		return False

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()		

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()

	@classmethod
	def find_by(cls, search):
		if search['email']:
			user = cls.query.filter_by(email=search['email']).first()
		elif search['username']:
			user = cls.query.filter_by(username=search['username']).first()
		elif search['id']:
			user = cls.query.filter_by(id=search['id']).first()
		else:
			return None
		if user:
			return user
		return None
