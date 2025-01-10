from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
api = Api(app)

class UserModel(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f"User(name = {self.name}, email = {self.email})"

# Validate data
user_args = reqparse.RequestParser()
user_args.add_argument('name', type=str, required=True, help="Name cannot be blank")
user_args.add_argument('email', type=str, required=True, help="Email cannot be blank")

userFields = {
    'id':fields.Integer,
    'name':fields.String,
    'email':fields.String,
}

class Users(Resource):
    @marshal_with(userFields)
    def get(self): # get method
        users = UserModel.query.all() # retrieving all the users from the database
        return users
    
    @marshal_with(userFields)
    def post(self): # post method
        args = user_args.parse_args()
        user = UserModel(name=args["name"], email=args["email"])
        db.session.add(user)
        db.session.commit()
        users = UserModel.query.all()
        return users, 201

# A User can be edited, deleted, and retrieved
class User(Resource):
    @marshal_with(userFields)
    def get(self, id):
       user = UserModel.query.filter_by(id=id).first() # retrieve a specific user from the database
       if not user:
        abort(404, "User not found")
        return user
    
    @marshal_with(userFields)
    def patch(self, id):
        args = user_args.parse_args()
        user = UserModel.query.filter_by(id=id).first() # retrieve a specific user from the database
        if not user:
            abort(404, "User not found")
        user.name = args["name"]
        user.email = args["email"] 
        db.session.commit()
        return user

    @marshal_with(userFields)
    def delete(self, id):
        user = UserModel.query.filter_by(id=id).first() # retrieve a specific user from the database
        if not user:
            abort(404, "User not found")
        db.session.delete(user)
        db.session.commit()
        users = UserModel.query.all()
        return users

api.add_resource(Users, '/api/users')
api.add_resource(User, '/api/users/<int:id>')

@app.route('/')
def home():
    return '<h1>Basic Flask Application</h1>'

if __name__ == '__main__':
    app.run(debug=True)
