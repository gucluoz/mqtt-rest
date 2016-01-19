from . import db
from sqlalchemy import desc

class Temprature(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  m1 = db.Column(db.String(100))
  m2 = db.Column(db.String(100))
  m3 = db.Column(db.String(100))
  m4 = db.Column(db.String(100))
  timestamp = db.Column(db.DateTime)
  value = db.Column(db.Float)

  def serialize(self):
    return {
      'm1': self.m1,
      'm2': self.m2,
      'm3': self.m3,
      'm4': self.m4,
      'value': self.value,
      'timestamp': self.timestamp
    }

  def __repr__(self):
    return '<Temprature {}/{}/{}/{}> -> {}'.format(self.m1, self.m2, self.m3, self.m4, self.value)

  def __init__(self,m1,m2,m3,m4):
    self.m1 = m1
    self.m2 = m2
    self.m3 = m3
    self.m4 = m4

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(60))
  password = db.Column(db.String(32))
  assets = db.relationship('Asset', backref='user', lazy='joined')

  def __repr__(self):
    return self.username

  def to_json(self, hasValues=None):
    result = '{'
    result += u'"username": "{}", '.format(self.username if None != self.username else '')
    result += u'"password": "{}", '.format(self.password if None != self.password else '')
    result += u'"assets": [%s]' % ','.join(map(lambda x:(x.to_json(hasValues=hasValues)),self.assets))
    result += '}'
    return result

  def get_assets(self, hasValues=None):
    return u'{"assets": [%s]}' % ','.join(map(lambda x:(x.to_json(hasValues=hasValues)),self.assets))

class Asset(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  identifier = db.Column(db.String(100))
  name = db.Column(db.String(100))
  address = db.Column(db.String(300))
  buildingItems = db.relationship('BuildingItem', backref='asset', lazy='joined')
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

  def __repr__(self):
    return self.name

  def to_json(self, hasValues=None):
    result = '{'
    result += u'"name": "{}", '.format(self.name if None != self.name else '')
    result += u'"identifier": "{}", '.format(self.identifier if None != self.identifier else '')
    result += u'"address": "{}", '.format(self.address if None != self.address else '')
    result += u'"buildingItems": [%s]' % ','.join(map(lambda x:(x.to_json(hasValues=hasValues)),self.buildingItems))
    result += '}'
    return result

  def get_building_items(self, hasValues=None):
    return u'{"buildingItems": [%s]}' % ','.join(map(lambda x:(x.to_json(hasValues=hasValues)),self.buildingItems))

class BuildingItem(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  identifier = db.Column(db.String(100))
  name = db.Column(db.String(100))
  sensors = db.relationship('Sensor', backref='buildingItem', lazy='joined')
  asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'))

  def __repr__(self):
    return self.name

  def to_json(self, hasValues=None):
    result = '{'
    result += u'"name": "{}", '.format(self.name if None != self.name else u'')
    result += u'"identifier": "{}", '.format(self.identifier if None != self.identifier else u'')
    result += u'"id": {}, '.format(self.id if None != self.id else u'')
    result += u'"sensors": [%s]' % ','.join(map(lambda x:(x.to_json(hasValues=hasValues)),self.sensors))
    result += '}'
    return result

  def get_sensors(self, hasValues=None):
    return u'{"sensors": [%s]}' % ','.join(map(lambda x:(x.to_json(hasValues=hasValues)),self.sensors))

class Sensor(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  identifier = db.Column(db.String(100))
  name = db.Column(db.String(100))
  buildingItem_id = db.Column(db.Integer, db.ForeignKey('building_item.id'))

  def __repr__(self):
    return self.name

  def to_json(self, hasValues=None):
    result = '{'
    result += u'"name": "{}", '.format(self.name if None != self.name else u'')
    result += u'"identifier": "{}"'.format(self.identifier if None != self.identifier else u'')
    if hasValues:
      latestValue = Temprature.query.filter_by(m1 = self.buildingItem.asset.user.username,
       m2 = self.buildingItem.asset.identifier,
       m3 = self.buildingItem.identifier,
       m4 = self.identifier).order_by(desc(Temprature.timestamp)).first()
      result += u',"value": {} '.format(latestValue.value if None != latestValue else u'0')
    result += '}'
    return result