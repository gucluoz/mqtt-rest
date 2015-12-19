from . import api
from flask import jsonify, request
from ..models import Temprature
import json
from .. import db
from datetime import datetime

@api.route('/')
def get_temps():
  temps = Temprature.query.all()
  return jsonify(temps = [temp.serialize() for temp in temps])

@api.route('/<m1>/<m2>/<m3>/<m4>')
def get_temp(m1,m2,m3,m4):
  temp = Temprature.query.filter_by(m1=m1,m2=m2,m3=m3,m4=m4).order_by(Temprature.timestamp.desc()).first()
  if temp:
    return jsonify(value=temp.serialize())
  return 'not found',404

@api.route('/<m1>/<m2>/<m3>/<m4>', methods=['POST'])
def post_temp(m1,m2,m3,m4):
  val = request.form.get('value')
  if not val:
    return 'value not present',403
  temp = Temprature(m1,m2,m3,m4)
  temp.value = val
  temp.timestamp = datetime.utcnow()
  db.session.add(temp)
  db.session.commit()

  return jsonify(temp = temp.serialize())