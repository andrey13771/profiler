from flask import request
from profiler_server.app import app, db
from profiler_server.app.models.models import Url
from profiler_server.app.logic.classify import classify_url


@app.route('/health')
def health():
    return {'status': 'ok'}


@app.route('/save_url', methods=['POST'])
def save_url():
    url = request.form['url']
    url = url.split('/')[2]
    if request.form['reason'] == 'navigate':
        prediction = classify_url(url)
        if prediction == -1:
            return {'message': 'suspicious url'}
    url = Url(url=url)
    db.session.add(url)
    db.session.commit()
    return {'message': 'saved'}