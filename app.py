import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from os import path
if path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'task_manager'
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

# print(os.environ.get("MONGO_URI"))
# app.secret_key = os.environ.get("MONGO_URI")

mongo = PyMongo(app)


@app.route('/get_tasks')
def get_tasks():
    return render_template("tasks.html",
    tasks=mongo.db.tasks.find())


@app.route('/add_task')
def add_task():
    return render_template("addtask.html",
    categories=mongo.db.categories.find())


@app.route('/insert_task', methods=['POST'])
def insert_task():
    tasks = mongo.db.tasks
    tasks.insert_one(request.form.to_dict())
    return redirect(url_for('get_tasks'))


@app.route('/edit_task/<task_id>')
def edit_task(task_id):
    _task = mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
    _categories = mongo.db.categories.find()
    category_list = [category for category in _categories]
    return render_template('edittask.html', task=_task, categories=category_list)


if __name__ == '__main__':
    app.run(host='0.0.0.0',
    port=5000,
    debug=True)
