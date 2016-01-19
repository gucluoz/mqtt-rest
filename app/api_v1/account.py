from . import api
from flask import jsonify
from ..models import User, Asset, BuildingItem, Sensor
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
  hasValues = ''
  try:
    hasValues = request.args.get('values')
  except:
    pass
  user = User.query.filter(User.username == request.authorization.username).first()
  return user.get_assets(hasValues = hasValues)

@api.route('/heartBeat')
@requires_auth
def heartBeat():
  return jsonify(authenticated=1)

@api.route('/getSensorValues')
@requires_auth
def get_sensor_values():
  try:
    buildingItemId = int(request.args.get('id'))
    user = User.query.filter(User.username == request.authorization.username).first()
    for a in user.assets:
      for b in a.buildingItems:
        if b.id == buildingItemId:
          return BuildingItem.query.get(buildingItemId).get_sensors(hasValues=1)
    return 'not authorized', 404
  except:
    return 'id required',401