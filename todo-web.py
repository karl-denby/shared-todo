from pymongo import MongoClient
from bottle import route, run, template

@route('/test')
@route('/todo')
def todo_list():
    connection = 'mongodb://localhost:27017'
    client = MongoClient(connection)    
    db = client['shared']
    col = db['todo']

    results = []
    for note in col.find():
        results.append(note)

    return template('item_list', items=results)

run()