import json
from datetime import datetime
from flask import request
from app import app, db
from app.models.models import User, TabInfo, InputInfo, KeyboardTiming
from app.logic.classify import predict_tab_info


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


@app.route('/save_tab_info', methods=['POST'])
def save_tab_info():
    user = User.query.filter_by(google_id=request.form['user']).first()
    url = request.form['url']
    # url = url.split('/')[2]  # TODO maybe also keep the other part?
    time = datetime.fromtimestamp(float(request.form['time']) / 1000)  # TODO add default timestamp
    tabs = int(request.form['tabCount'])
    lang = request.form['lang']
    prediction = predict_tab_info(user, url, time, tabs, lang)
    if prediction == -1:
        return {'message': 'suspicious'}
    info = TabInfo(user=user, url=url, timestamp=time, tab_count=tabs, lang=lang)
    db.session.add(info)
    db.session.commit()
    return {'message': 'safe'}


@app.route('/save_input_info', methods=['POST'])
def save_input_info():
    user = User.query.filter_by(google_id=request.form['user']).first()
    cpm = request.form['cpm']
    time = datetime.fromtimestamp(float(request.form['time']) / 1000)  # TODO add default timestamp
    # TODO some predictions
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
    # print('keypress', keypress)
    # print('keyup', keyup)
    # TODO predictions
    timings = KeyboardTiming(user=user, keypress=keypress, keyup=keyup, timestamp=time)
    db.session.add(timings)
    db.session.commit()
    return {'message': 'safe'}


# @app.route('/save_url', methods=['POST'])
# def save_url():
#     url = request.form['url']
#     url = url.split('/')[2]
#     if request.form['reason'] == 'navigate':
#         prediction = classify_url(url)
#         if prediction == -1:
#             return {'message': 'suspicious url'}
#     url = TabInfo(url=url)
#     db.session.add(url)
#     db.session.commit()
#     return {'message': 'saved'}
