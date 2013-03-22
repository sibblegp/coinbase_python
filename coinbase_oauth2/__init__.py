__author__ = 'gsibble'

from flask import Flask, render_template, request, make_response

from oauth2client.client import OAuth2WebServerFlow

APP = Flask(__name__)
APP.debug = True

from secrets import CALLBACK_URL, CLIENT_ID, CLIENT_SECRET

coinbase_client = OAuth2WebServerFlow(CLIENT_ID, 'all', 'all', 'http://www.paywithair.com/consumer_auth', auth_uri='https://www.coinbase.com/oauth/authorize', token_uri='https://www.coinbase.com/oauth/token')

@APP.route('/')
def register_me():

    auth_url = coinbase_client.step1_get_authorize_url('http://www.paywithair.com/consumer_auth')

    return render_template('register.jinja2', auth_url=auth_url)

@APP.route('/consumer_auth')
def receive_token():

    oauth_code = request.args['code']

    token = coinbase_client.step2_exchange(oauth_code)

    return make_response(token.to_json())

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=5010)