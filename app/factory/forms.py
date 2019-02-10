from flask_wtf import Form, RecaptchaField	
from wtforms import TextField, IntegerField, TextAreaField, SelectField, DateTimeField, SubmitField, validators, TextField, TextAreaField, SubmitField, validators, ValidationError, PasswordField
from .models import db, User


class SignupForm(Form):
  firstname = TextField("First name",  [validators.Required("Please enter your first name.")])
  lastname = TextField("Last name",  [validators.Required("Please enter your last name.")])
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  password = PasswordField('Password', [validators.Required("Please enter a password.")])
  #recaptcha = RecaptchaField()
  submit = SubmitField("Create account")
 
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      return False
     
    user = User.query.filter_by(email = self.email.data.lower()).first()
    if user:
      self.email.errors.append("That email is already taken")
      return False
    else:
      return True

class SigninForm(Form):
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  password = PasswordField('Password', [validators.Required("Please enter a password.")])
  #recaptcha = RecaptchaField()
  submit = SubmitField("Sign In")
   
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      return False
     
    user = User.query.filter_by(email = self.email.data.lower()).first()
    if user and user.check_password(self.password.data):
      return True
    else:
      self.email.errors.append("Invalid e-mail or password")
      return False

class DeliveryOrder(Form):
  name = TextField("Name*",[validators.Required("Please Enter the Customer Name.")])
  phone1 = TextField("Mobile Number*",[validators.Required("Please enter Mobile Number ex. 01234567890")])
  phone2 = TextField("Other Phone")
  email = TextField("Email")
  city = TextField("City")
  address = TextField("Address*")
  floor = TextField("Floor Number")
  lang = TextField("Language")
  condition = TextField("Condition")
  apartment = TextField("Apartment Number")
  address_comments = TextField("Address Comments")
  order_comments = TextField("Order Comments")
  number_of_pieces = IntegerField("Number of Pieces*", [validators.Required("Please Enter Only Number in Number of Pieces")])
  time_of_pickup = DateTimeField("Time of Pickup")
  time_of_delivery = DateTimeField("Time of Delivery")
  submit = SubmitField("Create Delivery Order")
