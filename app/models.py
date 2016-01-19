from . import db

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
  assets = db.relationship('Asset', backref='user', lazy='dynamic')

  def __repr__(self):
    return self.username

  def to_json(self):
    result = '"username": "{}", '.format(self.username if None != self.username else '')
    result += '"password": "{}", '.format(self.password if None != self.password else '')
    result += '"assets": {%s}' % ','.join(map(lambda x:(x.to_json()),self.assets))
    return result

  def get_assets(self):
    return '"assets": {%s}' % ','.join(map(lambda x:(x.to_json()),self.assets))

class Asset(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  identifier = db.Column(db.String(100))
  name = db.Column(db.String(100))
  address = db.Column(db.String(300))
  buildingItems = db.relationship('BuildingItem', backref='asset', lazy='dynamic')
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

  def __repr__(self):
    return self.name

  def to_json(self):
    result = '"name": "{}", '.format(self.name if None != self.name else '')
    result += '"identifier": "{}", '.format(self.identifier if None != self.identifier else '')
    result += '"address": "{}", '.format(self.address if None != self.address else '')
    result += '"buildingItems": {%s}' % ','.join(map(lambda x:(x.to_json()),self.buildingItems))
    return result

  def get_building_items(self):
    return '"buildingItems": {%s}' % ','.join(map(lambda x:(x.to_json()),self.buildingItems))

class BuildingItem(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  identifier = db.Column(db.String(100))
  name = db.Column(db.String(100))
  sensors = db.relationship('Sensor', backref='buildingItem', lazy='dynamic')
  asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'))

  def __repr__(self):
    return self.name

  def to_json(self):
    result = '"name": "{}", '.format(self.name if None != self.name else '')
    result += '"identifier": "{}", '.format(self.identifier if None != self.identifier else '')
    result += '"sensors": {%s}' % ','.join(map(lambda x:(x.to_json()),self.sensors))
    return result

  def get_sensors(self):
    return '"sensors": {%s}' % ','.join(map(lambda x:(x.to_json()),self.sensors))

class Sensor(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  identifier = db.Column(db.String(100))
  name = db.Column(db.String(100))
  buildingItem_id = db.Column(db.Integer, db.ForeignKey('building_item.id'))

  def __repr__(self):
    return self.name

  def to_json(self):
    result = '"name": "{}", '.format(self.name if None != self.name else '')
    result += '"identifier": "{}"'.format(self.identifier if None != self.identifier else '')
    return result