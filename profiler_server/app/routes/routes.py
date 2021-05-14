import os
import json
from datetime import datetime
from flask import request
from app import app, db
from app.models.models import User, TabInfo, InputInfo, KeyboardTiming
from app.logic.learning import predict_tab_info, predict_input_info, predict_kb_timings, train_base


@app.route('/')
@app.route('/health')
def health():
    return {'status': 'ok'}


@app.route('/get_user', methods=['POST'])
def get_user():
    user = User.query.filter_by(google_id=request.form['user']).first()
    return {'user': bool(user)}


@app.route('/create_user', methods=['POST'])
def create_user():
    user = User(google_id=request.form['user'], email=request.form['email'])
    db.session.add(user)
    db.session.commit()
    return {'created': True}


@app.route('/train_base', methods=['POST'])
def train_base():
    train_base(request.form['user'])


@app.route('/save_tab_info', methods=['POST'])
def save_tab_info():
    user = User.query.filter_by(google_id=request.form['user']).first()
    url = request.form['url']
    data = {'user': user, 'url': url}
    if request.form['reason'] == 'navigate':
        time = datetime.fromtimestamp(float(request.form['time']) / 1000)  # TODO add default timestamp
        tabs = int(request.form['tabCount'])
        lang = request.form['lang']
        prediction = predict_tab_info(request.form['user'], url, tabs, lang, time)
        if prediction == -1:
            return {'message': 'suspicious'}
        data = {**data, 'timestamp': time, 'tab_count': tabs, 'lang': lang}
    info = TabInfo(**data)
    db.session.add(info)
    db.session.commit()
    return {'message': 'safe'}


@app.route('/save_input_info', methods=['POST'])
def save_input_info():
    # legacy
    user = User.query.filter_by(google_id=request.form['user']).first()
    cpm = request.form['cpm']
    time = datetime.fromtimestamp(float(request.form['time']) / 1000)  # TODO add default timestamp
    prediction = predict_input_info(request.form['user'], cpm)
    if prediction == -1:
        return {'message': 'suspicious'}
    info = InputInfo(user=user, cpm=cpm, timestamp=time)
    db.session.add(info)
    db.session.commit()
    return {'message': 'safe'}

@app.route('/save_kb_timings', methods=['POST'])
def save_kb_timings():
    user = User.query.filter_by(google_id=request.form['user']).first()
    keypress = json.loads(request.form['keypress'])
    keyup = json.loads(request.form['keyup'])
    time = datetime.fromtimestamp(float(request.form['time']) / 1000) # TODO add default timestamp
    prediction = predict_kb_timings(request.form['user'], keypress, keyup)
    if prediction == -1:
        return {'message': 'suspicious'}
    timings = KeyboardTiming(user=user, keypress=keypress, keyup=keyup, timestamp=time)
    db.session.add(timings)
    db.session.commit()
    return {'message': 'safe'}
