from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://bd259fd4ca6c2c:b5d58082@us-cdbr-east-06.cleardb.net'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)

ma = Marshmallow(app)

class Task(db.Model):

    #Aqui van todos los campos a llenar en la base de datos de mysql

    id = db.Column(db.Integer, primary_key = True )
    title = db.Column(db.String(70), unique = True )
    consola = db.Column(db.String(70))
    description = db.Column(db.String(100))
    link = db.Column(db.String(100))

    def __init__(self, title, description, link, consola):
        self.consola = consola
        self.description = description
        self.link = link
        self.title = title

db.create_all()


class TaskSchema(ma.Schema):
    class Meta: 
        fields = ('id','title','description')

task_schema = TaskSchema()
tasks_schema = TaskSchema(many = True)

@app.route('/tasks', methods=['POST'])
def create_task():

    description = request.json['description']
    title = request.json['title']
    link = request.json['link']
    consola = request.json['consola']

    new_task = Task(title,description,link,consola)

    db.session.add(new_task)
    db.session.commit()


    return task_schema.jsonify(new_task)
   
@app.route('/tasks', methods=['GET'])
def get_task():
    all_tasks = Task.query.all()
    result = tasks_schema.dump(all_tasks)
    return jsonify(result)

@app.route('/tasks/<id>', methods=['PUT'])    
def update_task(id):
    task = Task.query.get(id)
    title = request.json['title']
    description = request.json['description']

    task.title = title
    task.description = description

    db.session.commit()
    return task_schema.jsonify(task)

@app.route('/tasks/<id>', methods=['DELETE'])    
def delete_task(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return task_schema.jsonify(task)





if __name__ == "__main__":
    app.run(debug = True)

