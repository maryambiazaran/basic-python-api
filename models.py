from app import db

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    task = db.Column(db.String(120))
    completed = db.Column(db.Boolean)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))

    def __init__(self, task, tag):
        self.task = task
        self.completed = False
        self.tag = tag

    def json_repr(self):
        output = {}
        output["id"] = self.id
        output["task"] = self.task
        return output

    # def __repr__(self):
    #     output = {}
    #     output[id] = self.id
    #     output[task] = self.task
    #     output[tag] = self.tag
    #     return output





class Tag(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(40), nullable = False, unique = True)
    todos = db.relationship('Todo', backref = 'tag')

    def __init__(self, name):
        self.name = name