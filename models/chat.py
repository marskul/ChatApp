
class ChatModel():

	def __init__(self, _id):
		self.chat_id = _id
		self.messages = []
		self.users = []

	def new_message(self, message):
		self.messages.append(message)
		return self.jsonify()

	def add_user(self, name):
		if name in self.users:
			return {'message': '{} is in chat already.'.format(name)}, 400
		self.users.append(name)
		return self.jsonify(), 200

	def remove_user(self, name):
		if name in self.users:
			self.users.remove(name)
			return self.jsonify(), 200
		return {'message': "No such user in chat"}, 404

	def check_if_user_in_chat(self, name):
		if name in self.users:
			return True
		return False

	def jsonify(self):
		return {'chat_id': self.chat_id, 'users': self.users, 'messages': self.messages}

class ChatList():

	def __init__(self):
		self.chats = []

	def check_if_chat_exists(self, chat_id):
		if chat_id in [chat['chat_id'] for chat in self.chats]:
			return True
		return False

	def find_chat_model(self, chat_id):
		for chat_model in [chat['chat_body'] for chat in self.chats if chat['chat_id'] == chat_id]:
			return chat_model
		return None

	def add_chat(self, chat_id):
		if self.check_if_chat_exists(chat_id):
			return {'message': 'Chat id {} already exists'.format(chat_id)}, 400
		self.chats.append({'chat_id': chat_id, 'chat_body': ChatModel(chat_id)})
		return {'chat list': [chat['chat_id'] for chat in self.chats]}

	def remove_chat(self, chat_id): 
		if self.check_if_chat_exists(chat_id):
			self.chats = [chat for chat in self.chats if chat['chat_id'] != chat_id]
			return {'chat list': [chat['chat_id'] for chat in self.chats]}
		return {'message': 'Chat id {} not exists'.format(chat_id)}, 404


