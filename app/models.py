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