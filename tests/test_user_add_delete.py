import os
import unittest
import json
from app import app
from tests.testmethods import TestMethods

class ChatTests(TestMethods):

	def setUp(self):
		self.app = app.test_client()
		self.app.testing = True	
		self.userName = "testuser"
		self.email = "testuser@mail.box"
		self.password = "zxcv"	

	def tearDown(self):
		pass

	def test_add_and_delete_user(self):
		content = json.dumps({"username": self.userName, "password": self.password, "email": self.email})
		#add (register) user 
		result = self.app.post('/register', 
				data=content,
				content_type='application/json',
				follow_redirects=True
			)
		self.assertEqual(result.status_code, 201)
		#log in as him
		self.token = self.user_login(self.email, self.password)
		content = json.dumps({"email": self.email})
		#and self-delete
		result = self.app.delete('/user', 
				data=content,
				content_type='application/json',
				headers={'authorization': self.token},
				follow_redirects=True
			)
		self.assertEqual(result.status_code, 201)		


if __name__ == '__main__':
    unittest.main()