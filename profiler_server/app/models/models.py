from datetime import datetime
from app import db
from sqlalchemy.dialects.postgresql import JSONB


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(32), index=True, unique=True)
    email = db.Column(db.String(128), unique=True)
    tab_info = db.relationship('TabInfo', backref='user', lazy='dynamic')
    input_info = db.relationship('InputInfo', backref='user', lazy='dynamic')
    kb_timing = db.relationship('KeyboardTiming', backref='user', lazy='dynamic')

    def __repr__(self):
        return f'<User> {self.google_id}'


class TabInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    url = db.Column(db.String(2048))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    tab_count = db.Column(db.Integer, index=True)
    lang = db.Column(db.String(16), index=True)

    def __repr__(self):
        return f'<TabInfo user: {self.user_id}, url:{self.url}, time: {self.timestamp}, ' \
               f'tabs: {self.tab_count}, lang: {self.lang}>'


class InputInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    cpm = db.Column(db.Float, index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return f'<InputInfo user: {self.user_id}, cpm: {self.cpm}>'


class KeyboardTiming(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    keypress = db.Column(JSONB)
    keyup = db.Column(JSONB)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return f'<KeyboardTiming> user:{self.user_id}, keypress: {self.keypress}, keyup: {self.keyup}'
