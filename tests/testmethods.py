import json
import unittest
from app import app

class TestMethods(unittest.TestCase):

	def user_login(self, _email, _password):
		content = json.dumps({"email": _email, "password": _password})
		result = self.app.post('/auth',
				data=content,
				content_type='application/json',
				follow_redirects=True
			)
		self.assertEqual(result.status_code, 200)
		if result.status_code != 200:
			return None
		response = json.loads(result.data.decode('utf-8'))
		return 'JWT {}'.format(response['access_token'])
