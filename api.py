from flask import Flask,request
from flask_restful import Resource, Api, reqparse
from requests import put, get

app = Flask(__name__)
api = Api(app)

# parser = reqparse.RequestParser()
# parser.add_argument('rate', type=int, help='Rate to charge for this resource')
# args = parser.parse_args()

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld,'/','/sayhi')

todos = {}

class TodoSimple(Resource):
    def get(self,todo_id):
        return {todo_id: todos[todo_id]},201, {'Etag': 'some-opaque-string'}

    def put(self,todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}



api.add_resource(TodoSimple, '/<string:todo_id>')


if __name__ == '__main__':
    app.run(debug = True)