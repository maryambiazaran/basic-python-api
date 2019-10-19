from app import app,db
from models import Todo, Tag
# from flask import request
from flask_restful import Resource, Api, reqparse, abort
import json

#app = Flask(__name__)
api = Api(app)

# parser = reqparse.RequestParser()
# parser.add_argument('rate', type=int, help='Rate to charge for this resource')
# args = parser.parse_args()

def get_incomplete_todos(tag = None):
    if tag is None:
        return Todo.query.filter_by(completed=False).order_by(-Todo.id).all()
    else:
        return Todo.query.filter_by(tag_id=tag.id, completed=True).order_by(-Todo.id).all()

def get_inactive_posts():
    return Todo.query.filter_by(completed=False).order_by(-Todo.id).all()


# TODOS = {
#     'todo1': {'task': 'build an API'},
#     'todo2': {'task': '????'},
#     'todo3': {'task': 'profit!s'},
# }

def abort_if_todo_doesnt_exist(todo_id):
    try:
        the_todo = Todo.query.filter_by(id=int(todo_id)).first()
        if the_todo:
            return None
        else:
            abort(404,message="TODO {} doesn't exist".format(todo_id))
    except TypeError:
        abort(404,message="TODO {} doesn't exist".format(todo_id))
    
    

parser = reqparse.RequestParser()
parser.add_argument('task')


# Todo
# shows a single todo item and lets you delete a todo item
class TodosController(Resource):
    def get(self,todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        the_todo = Todo.query.filter_by(id=int(todo_id)).first()
        print('===========================')
        print(the_todo.json_repr())
        return json.dumps(the_todo.json_repr()),200
        
        

    # def delete(self,todo_id):
    #     abort_if_todo_doesnt_exist(todo_id)
    #     del TODOS[todo_id]
    #     return '',204

    # def put(self,todo_id):
    #     args = parser.parse_args()
    #     task = {'task': args['task']}
    #     TODOS[todo_id] = task
    #     return task, 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks

# class TodoList(Resource):
#     def get(self):
#         return TODOS

    # def post(self):
    #     args = parser.parse_args()
    #     todo_id = int(max(TODOS.keys()).lstrip('todo'))+1
    #     todo_id = 'todo%i'%todo_id
    #     TODOS[todo_id] = {'task': args['task']}
    #     return TODOS[todo_id],201

# Actually setup the API
# api.add_resource(TodoList, '/todos')
api.add_resource(TodosController,'/todos/<todo_id>')


if __name__ == '__main__':
    app.run(debug = True)