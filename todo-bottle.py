from pymongo import MongoClient
from bottle import route, run

@route('/todo')
def todo_list():
    connection = 'mongodb://localhost:27017'
    client = MongoClient(connection)    
    db = client['shared']
    col = db['todo']

    results = []
    for note in col.find():
        results.append(note)

    return str(results)

run()