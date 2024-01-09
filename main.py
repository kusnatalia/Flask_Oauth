from flask import Flask, redirect, url_for, session, request
from authlib.integrations.flask_client import OAuth
from werkzeug.serving import make_ssl_devcert

GOOGLE_CLIENT_ID = '137159151203-se8tucbn4jihogbtk8udicnrdsr3mug2.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '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'
REDIRECT_URI = '/oauth2callback'

app = Flask(__name__)
app.secret_key = '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'
oauth = OAuth(app)

google = oauth.register(
    'google',
    base_url='https://www.google.com/accounts/',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    request_token_url=None,
    request_token_params={
        'scope': 'https://www.googleapis.com/auth/userinfo.email',
        'response_type': 'code'
    },
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_method='POST',
    access_token_params={'grant_type': 'authorization_code'},
    consumer_key=GOOGLE_CLIENT_ID,
    consumer_secret=GOOGLE_CLIENT_SECRET
)

make_ssl_devcert('./ssl', host='localhost')

@app.route('/login')
def login():
    return google.authorize_redirect(url_for('authorized', _external=True))

@app.route('/oauth2callback')
def authorized():
    token = google.authorize_access_token()
    user_info = google.parse_id_token(token)
    session['google_token'] = (token, '')
    return 'Logged in as: ' + user_info['email']

@app.route('/logout')
def logout():
    session.pop('google_token', None)
    return 'Logged out'

if __name__ == '__main__':
    app.run(debug=True, ssl_context=('ssl.crt', 'ssl.key'))






