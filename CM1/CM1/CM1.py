import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, render_template_string
from flask_github import GitHub

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , CM1.py


# Load default config and override config from an environment variable
app.config.update(dict(
	DATABASE=os.path.join(app.root_path, 'CM1.db'),
	SECRET_KEY='development key',
	USERNAME='admin',
	PASSWORD='default',
	# Set these values
	GITHUB_CLIENT_ID = 'fd7e54a1f4ac9becf832',
	GITHUB_CLIENT_SECRET = 'fff5546dbb5b35cee777bc779aec918b06348c09'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

# setup github-flask
github = GitHub(app)

def connect_db():
	"""Connects to the specific database."""
	rv = sqlite3.connect(app.config['DATABASE'])
	rv.row_factory = sqlite3.Row
	return rv

def get_db():
	"""Opens a new database connection if there is none yet for the current application context."""
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connect_db()
	return g.sqlite_db

def init_db():
	db = get_db()
	with app.open_resource('schema.sql', mode='r') as f:
		db.cursor().executescript(f.read())
	db.commit()

@app.cli.command('initdb')
def initdb_command():
	"""Initializes the database."""
	init_db()
	print('Initialized the database.')

@app.teardown_appcontext
def close_db(error):
	"""Closes the database again at the end of the request."""
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()






@app.route('/')
def index():
	if g.user:
		t = 'Hello! <a href="{{ url_for("user") }}">Get user</a> <a href="{{ url_for("repo") }}">Get repo</a> <a href="{{ url_for("logout") }}">Logout</a>'
	else:
		t = 'Hello! <a href="{{ url_for("login") }}">Login</a>'
	return render_template_string(t)


@github.access_token_getter
def token_getter():
	user = g.user
	if user:
		return "haha"

@app.route('/github-callback')
@github.authorized_handler
def authorized(access_token):
	print(request.args)
	next_url = request.args.get('next') or url_for('index')
	return redirect(next_url)

@app.route('/login')
def login():
	if session.get('user_id', None) is None:
		return github.authorize()
	else:
		return 'Already logged in'

@app.route('/logout')
def logout():
	session.pop('user_id', None)
	return redirect(url_for('index'))

@app.route('/user')
def user():
	json_data = github.get('user/repos')
	string = ""
	for j in json_data:
		for i in j:
			string += i+" : "+str(j[i])+"<br>"
			string += "<br><br>"
	return string

@app.route('/repo')
def repo():
	repo_dict = github.get('repos/cenkalti/github-flask')
	return str(repo_dict)
