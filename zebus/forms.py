from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField, BooleanField,TextAreaField
from wtforms.validators import DataRequired,Length,Email,EqualTo, ValidationError
from  zebus.models import User


class RegistrationForm(FlaskForm):
  username =  StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  confirm_password = PasswordField('Re-Enter Password', validators=[DataRequired(),EqualTo('password')])
  submit = SubmitField('Submit')


# validating mail and username
  def validate_username(self, username):

    user= User.query.filter_by(username=username.data).first()
    if user:
      raise ValidationError('Username already exists')

  def validate_email(self, email):

    user= User.query.filter_by(email=email.data).first()
    if user:
      raise ValidationError('Email already exists')



class LoginForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  remember = BooleanField('Remember Me')
  submit = SubmitField('Login')



class PostForm(FlaskForm):
  title= StringField('Title', validators=[DataRequired()])
  content= TextAreaField ('content', validators=[DataRequired()])
  submit= SubmitField('Post')

