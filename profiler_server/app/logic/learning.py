import os
import re
import pickle
from datetime import datetime
from urllib.parse import urlparse
from threading import Thread
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
# from sklearn.ensemble import IsolationForest
# from sklearn.svm import OneClassSVM
from sklearn.neighbors import LocalOutlierFactor
import joblib
import pandas as pd
from sqlalchemy import create_engine
from config import Config


STOPWORDS = ['http', 'https', 'www', 'com', 'org', 'net', 'int', 'edu', 'gov', 'mil', '']
DELIMITERS = ['&', '$', '+', ',', '/', ':', ';', '=', '?', '!', '@', '#', '-', '.', '_', '~', '%']
PATTERN = '|'.join(map(re.escape, DELIMITERS))


def process_url(url):
    url = urlparse(url.lower())
    url = url.netloc + url.path
    url = re.split(PATTERN, url)
    url = ''.join([word for word in url if word not in STOPWORDS])
    # ngrams
    n = 5
    url = [url[i : i + n] for i in range(len(url) - n + 1)]
    return url


def train_base(user):
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    df = pd.read_sql_table('tab_info', con=engine)
    urls = df.url
    pipeline = Pipeline([
        ('cv', CountVectorizer(analyzer=process_url)),
        ('lof', LocalOutlierFactor(novelty=True))
    ])
    pipeline.fit(urls)
    joblib.dump(pipeline, f'base{user}.sav')


def train_tab_info(user):
    return


def train_kb_timings(user):
    # placeholder
    return


def predict_tab_info(user, url, tabs, lang, time):
    path = os.path.abspath(os.path.dirname(__file__))
    if os.path.exists(os.path.join(path, 'tab_info{user}.sav')):
        clf = joblib.load(os.path.join(path, 'tab_info{user}.sav'))
        with open('lang_dict.p', 'rb') as f:
            lang_dict = pickle.load(f)
        if lang_dict.get(lang) is None:
            lang_dict[lang] = max(lang_dict.values()) + 1
        lang = lang_dict[lang]
        weekday = datetime.isoweekday(time)
        hour = time.hour + 1
        pred = clf.predict([url, tabs, lang, weekday, hour])
        if os.path.getmtime(os.path.join(path, 'tab_info{user}.sav') + 604800 < tdatetime.now().timestamp():
            th = Thread(target=train_tab_info, args=(user,))
            th.start()
    else:
        clf = joblib.load(os.path.join(path, 'base{user}.sav'))
        pred = clf.predict([url])
    return int(pred[0])


def predict_input_info(user, cpm):
    # legacy
    pass


def predict_kb_timings(user, keypress, keyup):
    #placeholder
    return
