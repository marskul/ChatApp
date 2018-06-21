from models.user import UserModel
from collections import defaultdict

def authenticate(email, password):
	ddict = defaultdict(str, {'email': email})
	user = UserModel.find_by(ddict)
	if user and user.email == email and user.password == password:
		return user

def identity(payload):
	user_id = payload['identity']
	ddict = defaultdict(int, {'id': user_id})
	return UserModel.find_by(ddict)