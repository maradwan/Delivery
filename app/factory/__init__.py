# -*- coding: utf-8 -*-

from flask import Flask

app = Flask(__name__)

app.secret_key = 'dfkdfjdmne3@!sdfakskdksd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@db/factory?charset=utf8'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


from .models import db, User
db.init_app(app)
db.create_all()

# Admin User 
if not User.query.filter_by(email = 'admin@admin.com').first():
   newuser = User('admin', 'admin', 'admin@admin.com', 'Quob4iiyieKie3hu', 1)
   db.session.add(newuser)
   db.session.commit()

# Test User
if not User.query.filter_by(email = 'test@test.com').first():
   newuser = User('test', 'test', 'test@test.com', 'aoho0Eeg', 0)
   db.session.add(newuser)
   db.session.commit()


import factory.routes
