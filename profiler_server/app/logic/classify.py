import os
import re
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
# from sklearn.ensemble import IsolationForest
# from sklearn.svm import OneClassSVM
from sklearn.neighbors import LocalOutlierFactor
import joblib
import pandas as pd
from sqlalchemy import create_engine
from profiler_server.config import Config

STOPWORDS = ['www', 'com', 'org', 'net', 'int', 'edu', 'gov', 'mil']
DELIMITERS = ['&', '$', '+', ',', '/', ':', ';', '=', '?', '@', '#', '-', '.', '_', '~']
PATTERN = '|'.join(map(re.escape, DELIMITERS))


def process_url(url):
    url = re.split(PATTERN, url)
    url = [word for word in url if word not in STOPWORDS]
    return url


def train():
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    df = pd.read_sql_table('url', con=engine)
    urls = df.url
    pipeline = Pipeline([
        ('bow', CountVectorizer(analyzer=process_url)),
        ('tfidf', TfidfTransformer()),
        ('lof', LocalOutlierFactor(novelty=True))
    ])
    pipeline.fit(urls)
    joblib.dump(pipeline, 'tfidf-lof.sav')


def classify_url(url):
    path = os.path.abspath(os.path.dirname(__file__))
    clf = joblib.load(os.path.join(path, 'tfidf-lof.sav'))
    pred = clf.predict((url, ))
    return int(pred[0])
