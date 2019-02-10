from factory import app
from flask import Flask, render_template, request, flash, session, url_for, redirect, Response
from .forms import SignupForm, SigninForm, DeliveryOrder
from .models import db, User, Delivery
from flask import Markup
from functools import wraps
from datetime import timedelta
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from werkzeug.exceptions import HTTPException


app.config['RECAPTCHA_PUBLIC_KEY'] = ''
app.config['RECAPTCHA_PRIVATE_KEY'] = ''


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)

def login_required(f):
   @wraps(f)
   def wrap(*args, **kwargs):
       if 'email' in session:
           return f(*args, **kwargs)
       else:
           return redirect(url_for('signin'))
   return wrap 


class ModelView(ModelView):
    def is_accessible(self):
        if not 'email' in session:
           raise HTTPException('', Response(
                "Please log in as Admin.", 401,))
        user = User.query.filter_by(email = session['email']).first()
        if not user.is_admin:
           raise HTTPException('', Response(
                "Please log in as Admin.", 401,))
        return True

class MyView(BaseView):
    @expose('/')
    def index(self):
        return redirect(url_for('profile'))

admin = Admin(app)
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Delivery, db.session))
admin.add_view(MyView(name='Dashboard', menu_icon_type='glyph', menu_icon_value='glyphicon-home'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/about')
def about():
  return render_template('about.html')


@app.route('/testdb')
@login_required
def testdb():
  if db.session.query("1").from_statement("SELECT 1").all():
    return 'It works.'
  else:
    return 'Something is broken.'

@app.route('/signup', methods=['GET', 'POST'])
@login_required
def signup():
  form = SignupForm()

  user = User.query.filter_by(email=session['email']).first()

  if not user.is_admin:
    return redirect(url_for('profile'))

  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signup.html', form=form)
    else:
      newuser = User(form.firstname.data, form.lastname.data, form.email.data, form.password.data, 0)
      db.session.add(newuser)
      db.session.commit()
       
   #   session['email'] = newuser.email
      return redirect(url_for('home'))
   
  elif request.method == 'GET':
    return render_template('signup.html', form=form)

@app.route('/profile')
@login_required
def profile():

  user = User.query.filter_by(email = session['email']).first()
  if 'email' in session and user.is_admin:
     return render_template('profile.html', is_admin=True)
   # return redirect("/admin", code=302)
  return render_template('profile.html')

  
@app.route('/delivery', methods=['GET', 'POST'])
@login_required
def delivery():
  form = DeliveryOrder()
  user = User.query.filter_by(email=session['email']).first()

  if request.method == 'POST':
    if form.validate() == False:
      return render_template('delivery.html', form=form)
    else:
      newdelivery = Delivery(form.phone1.data, form.phone2.data, form.name.data, form.email.data, form.city.data, form.address.data, form.floor.data, form.apartment.data, form.address_comments.data, form.order_comments.data, form.number_of_pieces.data, form.time_of_pickup.data, form.time_of_delivery.data , user.email, form.lang.data, form.condition.data)
      db.session.add(newdelivery)
      db.session.commit()
      flash('Record was successfully added')
      return redirect(url_for('profile'))

  elif request.method == 'GET':
    return render_template('delivery.html', form=form)

@app.route('/showdelivery')
@login_required
def showdelivery():
   return render_template('showdelivery.html', delivery = Delivery.query.all())

@app.route('/signout')
@login_required
def signout():
  session.pop('email', None)
  return redirect(url_for('home'))

@app.route('/signin', methods=['GET', 'POST'])
def signin():
  form = SigninForm()
  
  if 'email' in session:
     return redirect(url_for('profile')) 
 
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signin.html', form=form)
    else:
      session['email'] = form.email.data
      return redirect(url_for('profile'))
                 
  elif request.method == 'GET':
    return render_template('signin.html', form=form)
