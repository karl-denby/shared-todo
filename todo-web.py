import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bottle import route, run, template, static_file, debug, run, default_app
from bottle import request, response
from bottle import post, get, put, delete

import waitress
import json

load_dotenv()

@route('/')
def test():
    return static_file('vue/index2.html', root='.')


@post('/api/v1')
def data_create():
       
    data = request.json

    connection = os.environ.get('MONGO_CONNECTION_STRING', 'mongodb://localhost:27017')
    client = MongoClient(connection)
    db = client['shared']
    col = db['todo']

    col.insert_one(data)

    response.headers['Content-Type'] = 'application/json'
    return 'ok'


@get('/api/v1')
def data_read():
    connection = os.environ.get('MONGO_CONNECTION_STRING', 'mongodb://localhost:27017')
    client = MongoClient(connection)    
    db = client['shared']
    col = db['todo']

    results = []
    for result in col.find():
        results.append(result)

    response.content_type='application/json'
    return str(results)


@put('/api/v1/<data>')
def update_handler(data):
    pass


@delete('/api/v1/<title>')
def delete_handler(title):
    connection = os.environ.get('MONGO_CONNECTION_STRING', 'mongodb://localhost:27017')
    client = MongoClient(connection)
    db = client['shared']
    col = db['todo']

    col.delete_one({"title": title})

    return 'ok'


app = application = default_app()

if __name__ == '__main__':
    run(server='waitress', host = '127.0.0.1', port = 8000, debug=True, reloader=True)
