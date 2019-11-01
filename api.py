from app import app,db
from models import Todo, Tag
from flask import request, render_template,redirect
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
import json
from helpers import str2bool
import requests

#app = Flask(__name__)
api = Api(app)

# =======================================

tag_fields = {
    'id' : fields.Integer,
    'name': fields.String,
}

todo_fields = {
    'id' : fields.Integer,
    'task': fields.String,
    'completed': fields.Boolean,
    'category': fields.String(attribute='tag.name'),
}

# =======================================
# def validate_auth():
# 	auth = request.authorization
# 	if not auth:  # no header set
# 		abort(401)
# 	user = UserModel.query.filter_by(username=auth.username).first()
# 	if user is None or user.password != auth.password:
# 		abort(401)

# =======================================

def get_incomplete_todos(tag = None):
    if tag is None:
        return Todo.query.filter_by(completed=False).order_by(-Todo.id).all()
    else:
        return Todo.query.filter_by(tag_id=tag.id, completed=True).order_by(-Todo.id).all()

def get_complete_todos():
    return Todo.query.filter_by(completed=True).order_by(-Todo.id).all()

# =======================================

def abort_if_todo_doesnt_exist(todo_id):
    try:
        the_todo = Todo.query.filter_by(id=int(todo_id)).first()
        if the_todo:
            return None
        else:
            abort(404,message="TODO {} doesn't exist".format(todo_id))
    except TypeError:
        abort(404,message="TODO {} doesn't exist".format(todo_id))

def find_or_create_new_tag(tag_name):

    the_tag = Tag.query.filter_by(name=tag_name).first()
    if the_tag:
        return the_tag
    else:
        new_tag = Tag(tag_name)
        db.session.add(new_tag)
        db.session.commit()
        return new_tag

# =======================================

parser = reqparse.RequestParser()
parser.add_argument('task')
parser.add_argument('category')
parser.add_argument('completed', type=str2bool, default=None, help="Is the task complete?")

# =======================================

# Todo
# shows a single todo item and lets you delete a todo item
@api.resource('/api/todos/<todo_id>')
class TodosController(Resource):
    
    #GET
    @marshal_with(todo_fields, envelope='Todo')
    def get(self,todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        the_todo = Todo.query.filter_by(id=int(todo_id)).first()
        return the_todo,200

    #PUT
    @marshal_with(todo_fields, envelope='Todo')    
    def put(self,todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        the_todo = Todo.query.filter_by(id=int(todo_id)).first()
        args = parser.parse_args()
        if args['task']:
            the_todo.task = args['task']
        if args['completed'] != None:
            print('=============\n',args['completed'])
            the_todo.completed = bool(args['completed'])
        if args['category']:
            the_todo.tag = find_or_create_new_tag(args['category'])

        db.session.add(the_todo)
        db.session.commit()
        return the_todo, 201

    #DELETE
    def delete(self,todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        the_todo = Todo.query.filter_by(id=int(todo_id)).first()
        db.session.delete(the_todo)
        db.session.commit()
        return '', 204
        
# =======================================

# TodoList
# shows a list of all todos, and lets you POST to add new tasks

@api.resource('/api/todos')
class TodoListController(Resource):
    @marshal_with(todo_fields, envelope='Todos')
    def get(self):
        return Todo.query.all()
    
    @marshal_with(todo_fields, envelope='Todo')    
    def post(self):
        args = parser.parse_args()
        if args['task'] and args['category']:
            new_task_name = args['task']
            new_task_tag = find_or_create_new_tag(args['category'])
            new_todo = Todo(new_task_name,new_task_tag)
            db.session.add(new_todo)
            db.session.commit()
            return new_todo, 201
        else:
            abort(404,message="Bad user")




# Actually setup the API
# api.add_resource(TodoListController, '/todos')
# api.add_resource(TodosController,'/todos/<todo_id>')



@app.route('/')
def index():
    
    # GET REQUEST - INDIVIDUAL
    the_url = 'http://localhost:5000/api/todos'
    todo_id = 1
    if todo_id:
        rget = requests.get(url = the_url+'/'+str(todo_id))
    else:
        rget = requests.get(url = the_url)

    # print('----------------------------\n',rget.json())
    # return str(rget.json())
    return render_template('index.html',incomplete_todos = get_incomplete_todos(), completed_todos = get_complete_todos())
    

    # POST REQUEST - NEW TASKS
    # API_ENDPOINT2 = 'http://localhost:5000/api/todos'
    # data_2 = {'task':'do all the things',
    # 'category': 'good stuff'}
    # rpost = requests.post(url = API_ENDPOINT2, data = data_2)
    # pastebin_url = rpost.text 
    # print('----------------------------\n',pastebin_url)
    # return render_template('index.html')

    # PUT REQUEST - MODIFY TASK

@app.route('/update', methods = ['POST'])
def update_todo():
    todo_id = (request.form['todo-id'])
    API_ENDPOINT = 'http://localhost:5000/api/todos/'+todo_id
    current_stat = Todo.query.get(todo_id).completed
    put_data = {'completed' : not current_stat}
    r_put = requests.put(url = API_ENDPOINT, data = put_data)
    return redirect('/')


@app.route('/new-todo', methods = ['POST'])
def create_todo():
    API_ENDPOINT = 'http://localhost:5000/api/todos'
    todo_task = request.form['task']
    todo_tag = request.form['category']
    post_data = {'task' : todo_task,
    'category': todo_tag }
    r_post = requests.post(url = API_ENDPOINT, data = post_data)
    return redirect('/')




if __name__ == '__main__':
    
    app.run(debug = True)