from pymongo import MongoClient
from bottle import route, run, template, static_file, debug, run, default_app
from bottle import request, response
from bottle import post, get, put, delete
import gunicorn
import json


@route('/')
def test():
    return static_file('vue/index.html', root='.')


@post('/rest')
def data_create():
       
    data = {'Note': 'CRUD is fun!!!'}

    response.headers['Content-Type'] = 'application/json'
    return json.dumps(data)


@get('/rest')
def data_read():
    connection = 'mongodb://localhost:27017'
    client = MongoClient(connection)    
    db = client['shared']
    col = db['todo']

    results = []
    for result in col.find():
        results.append(result)

    response.content_type='application/json'
    return str(results)


@put('/rest/<data>')
def update_handler(name):
    pass


@delete('/rest/<data>')
def delete_handler(name):
    pass


app = application = default_app()

if __name__ == '__main__':
    run(server='gunicorn', host = '127.0.0.1', port = 8000, debug=True, reloader=True)
