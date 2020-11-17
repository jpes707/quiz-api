import os
import json
import sys
import pymongo
from time import time
from functools import wraps
from flask import request, abort, Flask, Response
from email.utils import formatdate
from random import shuffle
from mongo_config import questions_collection

app = Flask(__name__)


def date_time_string(timestamp=None):  # returns the current date and time formatted for a message header
    if timestamp is None:
        timestamp = time()
    return formatdate(timestamp, usegmt=True)


def verify_parameters(required_parameters):
    missing_parameters = []
    for param in required_parameters:
        if not request.args.get(param):
            missing_parameters.append(param)
    if missing_parameters:
        abort(get_api_response({'error_message': 'One or more required parameters was missing.', 'missing_parameters': missing_parameters}, 400))


def set_default_api_headers(res):
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Vary'] = 'Accept-Encoding'
    res.headers['Content-Type'] = 'application/json; charset=utf-8'


def get_api_response(obj, code=200):  # obj is a python list, dict, etc.
    res = Response(json.dumps(obj).encode('utf-8'), code)
    set_default_api_headers(res)
    return res


@app.route('/')
def index():
    return '<meta http-equiv="refresh" content="0; URL=https://github.com/jpes707/quiz-api/">'


@app.route('/get_question/')
def get_question():
    question_object = list(questions_collection.aggregate([{ '$sample': { 'size': 1 } }]))[0]
    del question_object['_id']
    shuffle(question_object['choices'])
    res = get_api_response(question_object)
    return res


if __name__ == '__main__':
    app_port = int(os.getenv('PORT')) if os.getenv('PORT') else 5000
    app.run(port=app_port)
