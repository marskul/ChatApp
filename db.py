from flask_sqlalchemy import SQLAlchemy
from models.chat import ChatList

db = SQLAlchemy()

chat_list = ChatList()