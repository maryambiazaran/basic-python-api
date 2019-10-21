from app import app,db
from models import Todo, Tag
# from flask import request
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
import json
from helpers import str2bool

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

def get_incomplete_todos(tag = None):
    if tag is None:
        return Todo.query.filter_by(completed=False).order_by(-Todo.id).all()
    else:
        return Todo.query.filter_by(tag_id=tag.id, completed=True).order_by(-Todo.id).all()

def get_inactive_posts():
    return Todo.query.filter_by(completed=False).order_by(-Todo.id).all()

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
@api.resource('/todos/<todo_id>')
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

# class TodoList(Resource):
#     @marshal_with(todo_fields, envelope='Todo')
#     # STILL NEED TO WORK ON THIS
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
# api.add_resource(TodosController,'/todos/<todo_id>')


if __name__ == '__main__':
    app.run(debug = True)