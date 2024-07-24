from flask import Flask, render_template, request, redirect, url_for
import redis
import json
app = Flask(__name__)

redis_client = redis.Redis(host='localhost', port=6379, db=0)


def deleteValues():
    todos = redis_client.lrange('todos', 3, -1)


def fetchTodosFromRedis():
    # Fetch all items from Redis
    todos = redis_client.lrange('todos', 0, -1)
    todos = [json.loads(item.decode('utf-8')) for item in todos]
    return todos


@app.route('/')
def index():
    todos = fetchTodosFromRedis()
    return render_template('index.html', len=len(todos), todos=todos)


@app.route('/save', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        # Here you can process the form data (e.g., save to database, send email, etc.)
        # For now, we'll just print it to the console
        print(f'Name: {name}')

        todos = fetchTodosFromRedis()
        todo = {"id": len(todos) + 1, "name": name}
        print(json.dumps(todo))
        redis_client.rpush('todos', json.dumps(todo))

        return redirect(url_for('index'))


@app.route('/delete/<name>', methods=['GET'])
def delete_item(name):
    print("looking for " + name)
    todos = fetchTodosFromRedis()
    for item in todos:
        print(item)
        if item["name"] == name:
            redis_client.lrem('todos', 0, json.dumps(item))
            break

    return redirect(url_for('index'))


@app.route('/change/<id>/<name>', methods=['GET'])
def get_change_item(id,name):
    return render_template('update.html', name=name, id = id)


@app.route('/update', methods=['POST'])
def update():
    print('update method ' + request.method)
    if request.method == 'POST':
        oldname = request.form['oldname']
        newname = request.form['newname']
        id = request.form['id']
        redis_client.lrem('todos', 0, json.dumps(oldname))
        todo = {"id": id, "name": newname}
        redis_client.rpush('todos', newname)
        return redirect(url_for('index'))
