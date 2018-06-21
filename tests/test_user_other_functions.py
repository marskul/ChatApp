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
		self.token = self.user_login("anna@mail.box", "qwert")	

	def tearDown(self):
		pass

	def search_user_by_data(self, _datatype, _data):
		content = json.dumps({_datatype: _data})
		result = self.app.post('/user',
				data=content,
				content_type='application/json',
				headers={'authorization': self.token},
				follow_redirects=True
			)
		self.assertEqual(result.status_code, 200)
		return json.loads(result.data.decode('utf-8'))

	def test_get_user_by_email(self):
		response = self.search_user_by_data("email", self.email)
		self.assertEqual(response['user'], self.userName)
		self.assertEqual(response['email'], self.email)

	def test_get_user_by_name(self):
		response = self.search_user_by_data("username", self.userName)
		self.assertEqual(response['user'], self.userName)
		self.assertEqual(response['email'], self.email)

	def test_get_userbase(self):
		result = self.app.get('/user',
				headers={'authorization': self.token},
				follow_redirects=True				
			)
		self.assertEqual(result.status_code, 200)

if __name__ == '__main__':
    unittest.main()
