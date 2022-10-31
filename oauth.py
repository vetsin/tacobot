import os, requests, string, random
from bottle import request, route, run, abort, redirect
from discord.utils import oauth_url
from discord import Permissions
from utils import load_env

state = ''.join(random.choice(string.ascii_letters) for i in range(10))


@route('/')
def index():
  redirect(oauth_url(os.environ['CLIENT_ID'], permissions=Permissions(8), redirect_uri='http://localhost:8080/oauth', scopes=['bot'], state=state))

@route('/oauth')
def exchange_code():
  code = request.query.code
  incstate = request.query.state
  if incstate != state:
    abort(401, "State mismatch somehow, are you being hacked...?")
  data = {
    'client_id': os.environ['CLIENT_ID'],
    'client_secret': os.environ['CLIENT_SECRET'],
    'grant_type': 'authorization_code',
    'code': code,
    'redirect_uri': 'http://localhost:8080/oauth'
  }
  headers = {'Content-Type': 'application/x-www-form-urlencoded'}
  r = requests.post('https://discord.com/api/oauth2/token', data=data, headers=headers)
  if 400 > r.status_code >= 200:
    rdata = r.json()
    access_token = rdata['access_token']
    return "Successfully added bot"
  print(r.text)
  abort(401, "Failed to use code to auth")


if __name__ == '__main__':
  load_env()
  assert 'CLIENT_ID' in os.environ
  assert 'CLIENT_SECRET' in os.environ
  assert 'BOT_TOKEN' in os.environ
  assert 'GUILD_ID' in os.environ, 'Requires the guild id we are going to add the bot to'

  print('Open http://localhost:8080 in your browser')
  run(host='localhost', port=8080, debug=True)
