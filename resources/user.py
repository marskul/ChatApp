from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.user import UserModel

class UserRegister(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument(
			'username',
			type=str,
			required=True,
			help="This field cannot be left blank"
		)
	parser.add_argument(
			'email',
			type=str, #check it!
			required=True,
			help="This field cannot be left blank"
		)
	parser.add_argument(
			'password',
			type=str,
			required=True,
			help="This field cannot be left blank"
		)
	
#new user register
	def post(self):
		data = UserRegister.parser.parse_args()
		if UserModel.find_by(data):
			return {"message": "{} already taken!".format(data['email'])}, 400
		user = UserModel(**data)
		if user.check_data():
			user.save_to_db()
			return {"message": "User created successfully."}, 201
		return {"message": "Missing required data!"}, 401

class User(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument(
			'username',
			type=str
		)
	parser.add_argument(
			'email',
			type=str
		)

	@jwt_required()
	def get(self):
		return {'users': [user.jsonify() for user in UserModel.query.all()]}

	@jwt_required()
	def post(self):
		data = User.parser.parse_args()
		user = UserModel.find_by(data)
		if user:
			return user.jsonify(), 200
		return {'message': "User not found."}, 404

	@jwt_required()
	def delete(self):
		data = User.parser.parse_args()
		user = UserModel.find_by(data)
		if not user:
			return {'message': "User not found."}, 404
		if not user.check_data():
			return {"message": "Missing required data!"}, 401
		user.delete_from_db()
		return {'message': 'User successfully deleted'}, 201
