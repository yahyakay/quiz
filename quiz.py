from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from config_quiz import Config
import random
import json

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = "quiz"


db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run(debug=True)

leaderBoard = {}
# playerName = ""
# results = []
# categoryName=""
# questions = []
users = []
class Quiz(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), nullable=False)
    answer = db.Column(db.String(100), nullable=False)
    choice1 = db.Column(db.String(100), nullable=False)
    choice2 = db.Column(db.String(100), nullable=False)
    choice3 = db.Column(db.String(100), nullable=False)
    choice4 = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    def to_dict(self):
        return {
                "id" : self.id,
                "question" : self.question,
                "answer" : self.answer,
                "choice1" : self.choice1,
                "choice2" : self.choice2,
                "choice3" : self.choice3,
                "choice4" : self.choice4,
                "category_id":self.category_id
        }


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)

class Username(db.Model):
    __tablename__ = 'usernames'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)


def getQuizbyQuestionId(quizId):
    return db.session.query(Quiz).filter_by(id = quizId).first()


def fetchUsernamesFromDB():
    # global users
    users = [i.name for i in Username.query.all()]
    print(users)


def fetchCategoriesFromDB():
    return Category.query.all()  # Fetch all data


def fetchQuizFromDB(categoryId, shuffle=False):
    print(categoryId)
    if categoryId == 0:
        return Quiz.query.all()
    else:
        all = db.session.query(Quiz).filter_by(category_id = categoryId).all()
        if shuffle == True:
            random.shuffle(all)
        return all[slice(20)]
class A:
    def toJSON(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4)

    def __init__(self, value):
        self.value = value

    def to_dict(self):
        return {'value': 'fdsfs'}

@app.route('/quiz')
def index():
    # global results
    # global questions
    session['results'] = []
    questions =fetchQuizFromDB(1,True)
    session['questions'] = [i.to_dict() for i in questions ]
    session['test'] = "test"
    categories = fetchCategoriesFromDB()
    return render_template('quiz.html', quizLen=len(session['questions']), quiz=session['questions'],  categoriesLen=len(categories), categories=categories)


@app.route('/total')
def total():
    print("results *******************")
    print(session['results'])
    print("results *******************")
    global leaderBoard
    totalCorrect = [i for i in session['results'] if i==1]
    leaderBoard[session['playerName']] = len(totalCorrect)
    sortedLeaderboard = sorted(leaderBoard.items(), key=lambda x: x[1], reverse=True)
    leaderBoard = dict(sortedLeaderboard)
    print("sortedLeaderboard *******************")
    print(sortedLeaderboard)
    print("sortedLeaderboard *******************")
    return render_template('results.html', category=session['categoryName'], totalLen=len(session['results']), totalCorrect=len(totalCorrect), leaderboard=leaderBoard, keys=list(leaderBoard.keys()), lenleaderboard=len(sortedLeaderboard))

@app.route('/save', methods=['POST'])
def submit():
    # global results
    session['results']=[]
    print("submit" + str(len(session['questions'])))
    if request.method == 'POST':
        category_id=int(request.form["category"])
        print("Category id requested is " + str (category_id))
        print("inside the if" + str(len(session['questions'])))
        for quiz in session['questions']:
            print(quiz)
            questionId='question_'+str(quiz['id'])
            print("after choice " + questionId)
            choice = request.form[questionId]
            print("after choice " + questionId)

            choice=choice.replace('A ','').replace('B ','').replace('C ','').replace('D ','')
            # [print(item.question) for item in quiz]
            if quiz != None and choice == quiz['answer'].replace('^ ',''):
                print(f"the correct answer is {choice}")
                temp=session['results']
                temp.append(1)
                session['results']=temp
            else:
                print(questionId + "=> answer = " + choice)
                session['results'].append(0)

    return redirect(url_for('total'))


@app.route('/categories/<id>', methods=['GET'])
def get_quiz_by_category(id):
    # global questions
    # global categoryName
    # global results
    categories = fetchCategoriesFromDB()
    questions = fetchQuizFromDB(categoryId=int(id),shuffle=True)
    session['questions'] = [i.to_dict() for i in questions ]
    session['results']=[]
    print("get_quiz_by_category " + str(len(session['questions'])))


    for item in categories:
        print(str(item.id) + "category name " +  item.name)
        if item.id == int(id):
            session['categoryName'] = item.name

    # print(products)
    return render_template('quiz.html', categoriesLen=len(categories), categories=categories, quizLen=len(session['questions']), quiz=session['questions'])

@app.route('/', methods=['GET', 'POST'])
def username():
    global users
    fetchUsernamesFromDB()
    if request.method == 'POST':
        # global playerName
        session['playerName'] = request.form['name']
        username = session['playerName']
        print(username)
        existingUsers=[i for i in users if i == session['playerName']]
        print("******************** " +session['playerName'])
        print(len(existingUsers))
        print("********************")
        if len(existingUsers) ==0:
            username = Username(name=session['playerName'])
            db.session.add(username)
            db.session.commit()
            users.append(session['playerName'])
            print("Player name *******************")
            print(session['playerName'])
            print("Player name *******************")


        return redirect(url_for('index'))
    return render_template('name_quiz.html')