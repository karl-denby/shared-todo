from bottle import route, run

@route('/todo')
def todo_list():
    result = ['test']
    return str(result)

run()