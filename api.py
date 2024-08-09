from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
api = Api(app)

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique=True, nullable=True)
    newClub = db.Column(db.String(80), unique=False, nullable=True)
    oldClub = db.Column(db.String(80), unique=False, nullable=True)
    country = db.Column(db.String(80), unique=False, nullable=True)

    def __repr__(self):
        return f"User(name = {self.name}, newClub = {self.newClub}, oldClub = {self.oldClub}, country = {self.country})"
    
user_args = reqparse.RequestParser()
user_args.add_argument('name', type=str, required=True, help="Name cannot be blank")
user_args.add_argument('newClub', type=str, required=True, help="New Club cannot be blank")
user_args.add_argument('oldClub', type=str, required=True, help="Old Club cannot be blank")
user_args.add_argument('country', type=str, required=True, help="Country cannot be blank")

userFields = {
    'id': fields.Integer,
    'name': fields.String,
    'newClub':fields.String,
    'oldClub':fields.String,
    'country':fields.String
}

class Users(Resource):
    @marshal_with(userFields)
    def get(self):
        users = UserModel.query.all()
        return users
    
    @marshal_with(userFields)   
    def post(self):
        args = user_args.parse_args()
        user = UserModel(name=args["name"], newClub=args["newClub"], oldClub=args["oldClub"], country=args["country"])
        db.session.add(user)
        db.session.commit()
        users = UserModel.query.all()
        return users, 201

class User(Resource):
    @marshal_with(userFields)   
    def get(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, "Your requested player is not found")
        return user
    
    @marshal_with(userFields)   
    def patch(self, id):
        args = user_args.parse_args()
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, "Your requested player is not found")
        user.name=args["name"]
        user.newClub=args["newClub"]
        user.oldClub=args["oldClub"]
        user.country=args["country"]
        db.session.commit()
        return user
    
    @marshal_with(userFields)   
    def delete(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, "Your requested player is not found")
        db.session.delete(user)
        db.session.commit()
        users = UserModel.query.all()
        return users

api.add_resource(Users, '/api/users/')
api.add_resource(User, '/api/users/<int:id>')

@app.route('/')
def home():
    return '<h1> Football Transfer Market 2024.</h1> <p> Welcome to the football transfer market 2024.</p>'

if __name__ == "__main__":
    app.run(debug=True)