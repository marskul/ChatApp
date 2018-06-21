from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
import time
from models.chat import ChatModel
from db import chat_list

class Chat(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument(
			'sender',
			type=str,
			required=True
		)

	parser_msg = parser.copy()
	parser_msg.add_argument(
			'message_body',
			type=str,
			required=True
		)

	@jwt_required()
	def get(self, name):	#returns if sender is in chat
		data = current_identity.username
		for eachChat in chat_list.chats:
			chat = eachChat['chat_body']
			if chat.check_if_user_in_chat(data):
				return chat.jsonify(), 200
		return {'message': 'ping'}, 200

	@jwt_required()
	def post(self, name):	#new user, if no chatwindow	new chatwindow	
		if not chat_list.check_if_chat_exists(name):
			chat_list.add_chat(name)
		data = Chat.parser.parse_args()
		return chat_list.find_chat_model(name).add_user(data['sender'])

	@jwt_required()
	def put(self, name):	#new message to existing chat
		if chat_list.check_if_chat_exists(name):
			data = Chat.parser_msg.parse_args()
			if chat_list.find_chat_model(name).check_if_user_in_chat(data['sender']):
				timestamp = time.time()			
				message = {
					'time': timestamp, 
					'sender': data['sender'], 
					'message_body': data['message_body']
					}
				return chat_list.find_chat_model(name).new_message(message), 200
			return {'message': '{} is not in chat'.format(data['sender'])}, 400
		return {'message': 'Chat id {} don\'t exist'.format(name)}, 404

	@jwt_required()
	def delete(self, name): #remove user, if no users left remove chatwindow			
		data = Chat.parser.parse_args()
		try:
			response = chat_list.find_chat_model(name).remove_user(data['sender'])
		except:
			return {'message': 'Chat {} don\'t exist!'.format(name)}, 404
		if not len(chat_list.find_chat_model(name).users):
			chat_list.remove_chat(name)
			return {'message': 'No users left, {} was terminated'.format(name)}, 200
		return response
