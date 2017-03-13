#!/usr/bin/env python3
from flask import Flask
from flask.ext.github import GitHub

app = Flask(__name__)
app.config['GITHUB_CLIENT_ID'] = 'fd7e54a1f4ac9becf832'
app.config['GITHUB_CLIENT_SECRET'] = 'fff5546dbb5b35cee777bc779aec918b06348c09'

# For GitHub Enterprise
#app.config['GITHUB_BASE_URL'] = 'https://HOSTNAME/api/v3/'
#app.config['GITHUB_AUTH_URL'] = 'https://HOSTNAME/login/oauth/'

github = GitHub(app)


@app.route("/")
def hello():
    return "Hello World!"

@app.route('/login')
def login():
    return github.authorize()

@app.route('/github-callback')
@github.authorized_handler
def authorized(oauth_token):
    next_url = request.args.get('next') or url_for('index')
	if oauth_token is None:
		flash("Authorization failed.")
		return redirect(next_url)
	
	user = User.query.filter_by(github_access_token=oauth_token).first()
	if user is None:
		user = User(oauth_token)
		db_session.add(user)
	user.github_access_token = oauth_token
	db_session.commit()
	return redirect(next_url)

if __name__ == "__main__":
	app.run()
