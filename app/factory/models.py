from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@db/factory?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
  __tablename__ = 'users'
  uid = db.Column(db.Integer, primary_key = True)
  firstname = db.Column(db.String(100))
  lastname = db.Column(db.String(100))
  email = db.Column(db.String(120), unique=True)
  pwdhash = db.Column(db.String(120))
  is_admin = db.Column(db.Boolean, default=False)


  def __init__(self, firstname, lastname, email, password, is_admin):
    self.firstname = firstname.title()
    self.lastname = lastname.title()
    self.email = email.lower()
    self.set_password(password)
    self.is_admin = is_admin

  def set_password(self, password):
    self.pwdhash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.pwdhash, password)


class Delivery(db.Model):
  __tablename__ = 'delivery'
  id = db.Column(db.Integer, primary_key = True) 
  created_at = db.Column(db.DateTime, index=True, default=datetime.now,nullable=False)
  is_finished = db.Column(db.Boolean, default=False)
  phone1 = db.Column(db.String(120))
  phone2 = db.Column(db.String(120))
  name = db.Column(db.String(120))
  email = db.Column(db.String(120))
  city = db.Column(db.String(120))
  address = db.Column(db.String(120))
  floor = db.Column(db.String(120))
  apartment = db.Column(db.String(120))
  address_comments = db.Column(db.String(120))
  order_comments = db.Column(db.String(120))
  number_of_pieces = db.Column(db.BigInteger)
  time_of_pickup = db.Column(db.DateTime, index=True, default=datetime.now,nullable=False)
  time_of_delivery = db.Column(db.DateTime, index=True, default=datetime.now,nullable=False)
  creator_name = db.Column(db.String(120), db.ForeignKey('users.email'))
  lang  = db.Column(db.String(120))
  condition  = db.Column(db.String(120))

  

  def __init__(self, phone1, phone2, name, email, city, address, floor, apartment, address_comments, order_comments, number_of_pieces, time_of_pickup, time_of_delivery, creator_name, lang, condition):
    self.phone1 = phone1
    self.phone2 = phone2
    self.name = name
    self.email = email
    self.city = city
    self.address  = address 
    self.floor = floor
    self.apartment = apartment
    self.address_comments = address_comments
    self.order_comments = order_comments
    self.number_of_pieces = number_of_pieces
    self.time_of_pickup = time_of_pickup
    self.time_of_delivery = time_of_delivery
    self.creator_name = creator_name
    self.lang = lang
    self.condition = condition
