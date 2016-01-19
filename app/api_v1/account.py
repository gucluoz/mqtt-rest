from . import api
from flask import jsonify
from ..models import User, Asset
from .. import db
from functools import wraps
from flask import request, Response
import md5

def check_auth(username, password):
    password_hash = md5.new(password).hexdigest().lower()
    return User.query.filter_by(username=username, 
      password=password_hash).count() > 0

def notAuthorizedError():
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return notAuthorizedError()
        return f(*args, **kwargs)
    return decorated

@api.route('/getAssets')
@requires_auth
def getAssets():
  user = User.query.filter(User.username == request.authorization.username).first()
  return user.get_assets()

@api.route('/heartBeat')
@requires_auth
def heartBeat():
  return jsonify(authenticated=1)