from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run(debug=True)

class Todos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)

class Ethnicity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ethno = db.Column(db.String(250), nullable=False)

class Genders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
class Students(db.Model):
    StudentID = db.Column(db.Integer, primary_key=True)
    Age = db.Column(db.Integer)
    Gender = db.Column(db.Integer, db.ForeignKey('Genders.id'))
    Ethnicity = db.Column(db.Integer, db.ForeignKey('Ethnicity.id'))
    ParentalEducation = db.Column(db.Integer)
    StudyTimeWeekly = db.Column(db.Integer)
    Absences = db.Column(db.Integer)
    Tutoring = db.Column(db.Integer)
    ParentalSupport = db.Column(db.Integer)
    Extracurricular = db.Column(db.Integer)
    Sports = db.Column(db.Integer)
    Music = db.Column(db.Integer)
    Volunteering = db.Column(db.Integer)
    GPA = db.Column(db.Integer)
    GradeClass = db.Column(db.Integer)
#     todos = redis_client.lrange('todos', 3, -1)


def fetchTodosFromDB():
    todos = Todos.query.all()  # Fetch all users
    # Fetch all items from Redis
    # todos = redis_client.lrange('todos', 0, -1)
    # todos = [json.loads(item.decode('utf-8')) for item in todos]
    return todos

def fetchStudentsFromDB():
    students=(db.session.query(Students, Genders, Ethnicity)
              .join(Genders, Students.Gender==Genders.id)
              .join(Ethnicity, Students.Ethnicity==Ethnicity.id)
              .add_columns(Students.StudentID,Students.Age,Genders.name,Ethnicity.ethno,Students.ParentalEducation,Students.StudyTimeWeekly,Students.Absences,Students.Tutoring,Students.ParentalSupport,Students.Extracurricular,Students.Sports,Students.Music,Students.Volunteering,Students.GPA,Students.GradeClass).paginate(page=1, per_page=3000).items)
    print(students)
    return students
    # Fetch all users

@app.route('/todos')
def index():
    todos = fetchTodosFromDB()
    return render_template('index.html', len=len(todos), todos=todos)


@app.route('/')
def loadStudents():
    students = fetchStudentsFromDB()
    return render_template('loadData.html', len=len(students), students=students)


@app.route('/save', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        todo = Todos(name=name)
        db.session.add(todo)
        db.session.commit()
        # Todos.query.insert(name)
        # Here you can process the form data (e.g., save to database, send email, etc.)
        # For now, we'll just print it to the console
        # print(f'Name: {name}')

        # todos = fetchTodosFromDB()
        # todo = {"id": len(todos) + 1, "name": name}
        # print(json.dumps(todo))
        # redis_client.rpush('todos', json.dumps(todo))

        return redirect(url_for('index'))


@app.route('/delete/<name>', methods=['GET'])
def delete_item(name):
    print("looking for " + name)
    todos = fetchTodosFromDB()
    for item in todos:
        print(item.id)
        print(item.name)
        if item.name == name:
            db.session.delete(item)
            db.session.commit()
            # redis_client.lrem('todos', 0, json.dumps(item))
            break

    return redirect(url_for('index'))


@app.route('/change/<id>/<name>', methods=['GET'])
def get_change_item(id, name):
    return render_template('update.html', name=name, id=id)


@app.route('/update', methods=['POST'])
def update():
    print('update method ' + request.method)
    if request.method == 'POST':
        newname = request.form['newname']
        id = request.form['id']
        todo = Todos.query.get_or_404(id)
        todo.name = newname
        db.session.commit()
        # redis_client.lrem('todos', 0, json.dumps(oldname))
        todo = {"id": id, "name": newname}
        # redis_client.rpush('todos', newname)
        return redirect(url_for('index'))


