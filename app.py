from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from flask_cors import CORS

from security import authenticate, identity
from resources.user import UserRegister, User
from resources.chat import Chat

from db import db


app = Flask(__name__)

CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'hr7boc3qnfdcwqpcyr82' #jwt secret key
app.config['JWT_AUTH_USERNAME_KEY'] = 'email'
api = Api(app)


@app.before_first_request
def create_tables():
	db.create_all()

jwt = JWT(app, authenticate, identity)

#endpoints
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user')
api.add_resource(Chat, '/chat/<string:name>')

db.init_app(app)

if __name__ == '__main__':
	app.run(port=5666, debug=True)