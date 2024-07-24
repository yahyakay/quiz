from flask import Flask, render_template
import requests
import json

app = Flask(__name__)

def get_meme(taskId):
    url = "https://jsonplaceholder.typicode.com/todos/"+taskId
    response = json.loads(requests.request("GET", url).text)
    print(response)
    id = response["userId"]
    title = response["title"]
    completed = response["completed"]
    return id,title, completed

@app.route("/<taskId>")
def index(taskId):
   id,  title, completed = get_meme(taskId)
   #return render_template("meme_index.html", id=id, title=title, completed=completed)
   return render_template("meme_index.html")



