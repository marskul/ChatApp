import os
import unittest
import json
from app import app
from tests.testmethods import TestMethods

class ChatTests(TestMethods):

	def setUp(self):
		self.app = app.test_client()
		self.app.testing = True	
		self.userName = "anna"
		self.email = "anna@mail.box"
		self.password = "qwer"
		self.chatNr = "654321"
		self.token = self.user_login(self.email, self.password)	
		#user is not in chat
		self.assertFalse(self.if_user_in_chat())
		#user joins chat
		self.assertEqual(self.add_user_to_chat(), 200)

	def tearDown(self):
		#user removes himself from chat
		self.assertEqual(self.delete_user_from_chat(self.userName), 200)

	def if_user_in_chat(self):
		result = self.app.get('/chat/' + self.chatNr,
				headers={'authorization': self.token},
				follow_redirects=True
			)
		self.assertEqual(result.status_code, 200)
		response = json.loads(result.data.decode('utf-8'))
		try:
			if response['chat_id'] == self.chatNr:
				return True
		except:
			return False

	def add_user_to_chat(self):
		content = json.dumps({"sender": self.userName})
		result = self.app.post('/chat/' + self.chatNr, 
				data=content,
				content_type='application/json',
				headers={'authorization': self.token},
				follow_redirects=True
			)
		return result.status_code	

	def send_message_to_chat(self, _chatnr):
		content = json.dumps({"sender": self.userName, "message_body": "test message"}) 
		result = self.app.put('/chat/' + _chatnr, 
				data=content,
				content_type='application/json',
				headers={'authorization': self.token},
				follow_redirects=True
			)		
		return result.status_code

	def delete_user_from_chat(self, _name):
		content = json.dumps({"sender": _name})
		result = self.app.delete('/chat/' + self.chatNr, 
				data=content,
				content_type='application/json',
				headers={'authorization': self.token},
				follow_redirects=True
			)		
		return result.status_code


	def test_join_chat_send_message_leave_chat(self):
		#sending message to chat
		self.assertEqual(self.send_message_to_chat(self.chatNr), 200)	

	def test_join_leave_chat(self):
		#checking if user joined
		self.assertTrue(self.if_user_in_chat())

	def test_message_to_another_chat(self):	
		#user fails to send message to another chat
		self.assertEqual(self.send_message_to_chat("162534"), 404)	

	def test_remove_nonexisting_user(self):
		#user tries to remove other nonexisting user from chat
		self.assertEqual(self.delete_user_from_chat("ambrozy"), 404)

	def test_double_joining_chat(self):
		#user fails to join chat in whitch he is already
		self.assertEqual(self.add_user_to_chat(), 400) 

if __name__ == '__main__':
    unittest.main()