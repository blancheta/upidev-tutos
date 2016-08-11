# -*- coding:utf-8 -*- 
from flask_login import UserMixin
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

# On créé notre modèle User


class Meal(db.Document):
	name = db.StringField(default='')

	def __str__(self):
		return self.name


class User(db.Document, UserMixin):
	email = db.StringField()
	password = db.StringField()
	meals = db.ListField(db.ReferenceField(Meal))

	def set_password(self, password):
		self.password = generate_password_hash(password)

	def check_password(self, passwd):
		return check_password_hash(self.password, passwd)
