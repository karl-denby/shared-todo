from pymongo import MongoClient
from bottle import route, run, template, response, static_file, debug

@route('/')
def test():
    return static_file('vue/index.html', root='.')

@route('/data')
def todo_list():
    connection = 'mongodb://localhost:27017'
    client = MongoClient(connection)    
    db = client['shared']
    col = db['todo']

    results = []
    for result in col.find():
        results.append(result)

    response.content_type='application/json'
    return str(results)

debug(True)
run(reloader=True)