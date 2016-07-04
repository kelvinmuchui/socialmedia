from flask_wtf import Form

from wtforms import StringField, PasswordField
from wtforms.validators import(DataRequired,Regexp, Email,
Length, EqualTo)
from models import User


def name_exists(form, field):
	if User.select().where(User.username == field.data).exists():
		raise ValidationError('User with that name already exists.')

def email_exists(form, field):
	if User.select().where(User.username == field.data).exists():
		raise ValidationError('User with that name already exists.')


class RegisterForm(Form):
	username = StringField(
        'Username', 
         validators = [
           DataRequired(),
           Regexp(
           	r'^[ a-zA-Z0-9_]+$',
           	message = ("username should be one word, letters, "
           		" numbers, andd underscores only")
           	),
           	name_exists])

	email = StringField(

    	'Email', 
    	validators= [
    	    DataRequired(),
    	    Email(),
    	    email_exists])
	password =  PasswordField(
        'Password',
        validators= [
            DataRequired(),
            Length(min = 2),
            EqualTo('password2', message ='Passwordmust match')]
    	)
	password2 = PasswordField(
    	'Confirm Password',
    	validators=[DataRequired()])
class LoginForm(Form):
	email = StringField('Email', validators = [DataRequired(), Email()])
	password = PasswordField('Password', validators = [DataRequired()])