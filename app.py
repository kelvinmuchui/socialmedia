from flask import(Flask, g, render_template, flash, redirect,url_for)
from flask.ext.bcrypt import check_password_hash
from flask.ext.login import (LoginManager, login_user, logout_user,
	login_required)

import forms 
from forms import User
import models

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = 'muchuikelvin'
 

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.log_view = 'login'

@login_manager.user_loader
def load_user(userid):
 	try:
 		return models.User.get(models.User.id == userid)
 	except models.DoesNotExist:
 		return None

@app.before_request
def before_request():
	"""Connect to the database before each request."""
	g.db = models.DATABASE
	g.db.connect()


@app.after_request
def after_request(response):
	"""Close the database connection after each request"""
	g.db.close()
	return response


@app.route('/register',methods= ('GET', 'POST'))
def register():
	form = forms.RegisterForm()
	if form.validate_on_submit():
		flash('you registered',"success")
		modells.User.create_user(
			username = form.username.data,
			email = form.email.data,
			password = formm.password.data)
		return redirect(url_for('index'))
	return render_template('register.html', form = form)

@app.route('/login', methods = ('GET', 'POST'))
def login():
	form = forms.LoginForm()
	if form.validate_on_submit():
		try:
			user = models.User.get(models.User.email == form.email.data)
		except models.DoesNotExist:
			flash("you email or password doesn't match", "error")

		else:
			if check_password_hash(user.password, form.password.data):
				load_user(user)
				flash("you have been loged in")
				return redirect(url_for('index'))
			else:
				flash("you email or password doesn't match", "error")
	return render_template('login.html', form = form)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	flash("You've loged out ! wellcome back")
	return redirect(url_for('index'))

@app.route('/')
def index():
	return'Hey'

if __name__ == '__main__':
	models.initialize()
	try:
		models.User.create_User(
			username = 'kelvin',
			email = 'muchuikelvin423@gmail.com',
			password = 'password',
			admin = True

			)
	except ValueError:
		pass
    
	app.run(debug = DEBUG, host = HOST, port = PORT)

