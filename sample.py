#!/usr/bin/env python3

from flask import Flask, request, g, session, redirect, url_for
from flask import render_template_string
from flask_github import GitHub
from flask_bootstrap import Bootstrap

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


import json

DATABASE_URI = 'sqlite:////tmp/github-flask.db'
SECRET_KEY = 'development key'
DEBUG = True

# Set these values
GITHUB_CLIENT_ID = 'fd7e54a1f4ac9becf832'
GITHUB_CLIENT_SECRET = 'fff5546dbb5b35cee777bc779aec918b06348c09'

# setup flask
app = Flask(__name__)
app.config.from_object(__name__)

# setup github-flask
github = GitHub(app)

# setup sqlalchemy
engine = create_engine(app.config['DATABASE_URI'])
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
	Base.metadata.create_all(bind=engine)


class User(Base):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True)
	username = Column(String(200))
	github_access_token = Column(String(200))

	def __init__(self, github_access_token):
		self.github_access_token = github_access_token


@app.before_request
def before_request():
	g.user = None
	if 'user_id' in session:
		g.user = User.query.get(session['user_id'])


@app.after_request
def after_request(response):
	db_session.remove()
	return response


@app.route('/')
def index():
	if g.user:
		t = 'Hello! <a href="{{ url_for("user") }}">Get user</a> <a href="{{ url_for("repo") }}">Get repo</a>'\
			'<a href="{{ url_for("logout") }}">Logout</a>'
	else:
		t = 'Hello! <a href="{{ url_for("login") }}">Login</a>'

	return render_template_string(t)


@github.access_token_getter
def token_getter():
	user = g.user
	if user is not None:
		return user.github_access_token


@app.route('/github-callback')
@github.authorized_handler
def authorized(access_token):
	next_url = request.args.get('next') or url_for('index')
	if access_token is None:
		return redirect(next_url)

	user = User.query.filter_by(github_access_token=access_token).first()
	if user is None:
		user = User(access_token)
		db_session.add(user)
	user.github_access_token = access_token
	db_session.commit()

	session['user_id'] = user.id
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
#	data = json.loads(json_data)
	for j in json_data:
#		s = str(j).replace("'", '"')
#		print(s)
#		data = json.loads(s)
		for i in j:
#			print(data[i])
			string += i+" : "+str(j[i])+"<br>"
		string += "<br><br>"
#	return str(github.get('user/repos'))
	return string

@app.route('/repo')
def repo():
	repo_dict = github.get('repos/cenkalti/github-flask')
	return str(repo_dict)

###########################################################
#spotify
@app.route('/makeup')
def makeup(dictionary):
	return redirect()


from flask import render_template, Flask
from datafoo import spotify

app = Flask(__name__)

@app.route('/')
def homepage():
    html = render_template('landing.html')
    return html

@app.route('/search/<name>')
def search(name):
    data = spotify.search_by_artist_name(name)
    api_url = data['artists']['href']
    items = data['artists']['items']
    # html = render_template('search.html', artist_name=name, results=items, api_url=api_url)
    return html

@app.route('/artist/<id>')
def artist(id):
    artist = spotify.get_artist(id)

    if artist['images']:
        image_url = artist['images'][0]['url']
    else:
        image_url = '/static/images/happy.png'

    tracksdata = spotify.get_artist_top_tracks(id)
    tracks = tracksdata['tracks']

    artistsdata = spotify.get_related_artists(id)
    relartists = artistsdata['artists']
    html = render_template('makeup.html', artist=artist, image_url=image_url, tracks=tracks)
    return html


if __name__ == '__main__':
	init_db()
	app.run(debug=True)