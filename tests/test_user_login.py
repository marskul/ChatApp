import os
import unittest
import json
from app import app

class ChatTests(unittest.TestCase):

	def setUp(self):
		self.app = app.test_client()
		self.app.testing = True		

	def tearDown(self):
		pass

	def test_user_login(self):
		result = self.app.post('/auth', 
				data='{"email": "anna@mail.box", "password": "qwer"}',
				content_type='application/json',
				follow_redirects=True
			)
		self.assertEqual(result.status_code, 200)

	def test_login_wrong_user(self):
		result = self.app.post('/auth', 
				data='{"email": "random@what.ever", "password": "wrong"}',
				content_type='application/json',
				follow_redirects=True
			)
		self.assertEqual(result.status_code, 401)

	def test_login_wrong_password(self):
		result = self.app.post('/auth', 
				data='{"email": "anna@mail.box", "password": "wrong"}',
				content_type='application/json',
				follow_redirects=True
			)
		self.assertEqual(result.status_code, 401)

if __name__ == '__main__':
    unittest.main()