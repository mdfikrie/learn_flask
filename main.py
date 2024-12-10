# Import library
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize Flask
app = Flask(__name__)

# Configure database (before initializing SQLAlchemy)
basedir = os.path.dirname(os.path.abspath(__file__))
database = "sqlite:///" + os.path.join(basedir, "db.sqlite")
app.config["SQLALCHEMY_DATABASE_URI"] = database

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Initialize other Flask extensions
api = Api(app)
CORS(app)

# Define database model
class ModelDatabase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    address = db.Column(db.TEXT)

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False

# Create database tables within the app context
with app.app_context() : db.create_all()

# Define API resource
class ExampleResource(Resource):
    def get(self):
        # menampilkan data dari database
        query = ModelDatabase.query.all()

        # melakukan iterasi
        response = [{"id":data.id, "name":data.name, "age":data.age, "address":data.address} for data in query]

        return {
            "status":200,
            "message": "success",
            "data": response
        }, 200

    def post(self):
        if request.is_json:
            data = request.get_json()
            name = data.get('name')
            age = data.get('age')
            address = data.get('address')
        else:
            name = request.form['name']
            age = request.form['age']
            address = request.form['address']

        model = ModelDatabase(name=name, age=age, address=address)
        if model.save():
            response = {"code": 200, "message": "success"}
        else:
            response = {"code": 500, "message": "failed to save data"}
        return response, 200
    
    def delete(self):
        query = ModelDatabase.query.all()
        for data in query:
            db.session.delete(data)
            db.session.commit()

        return {"status":200,"message":"success"}, 200
    
class UpdateResource(Resource):
    def get(self, id):
        # konsumsi id untuk query di database
        data = ModelDatabase.query.get(id)
        response = {
            "id": data.id,
            "name":data.name,
            "age":data.age,
            "address":data.address
        }
        return {
            "status":200,
            "message": "success",
            "data": response
        }, 200
    
    def put(self, id):
        data = request.get_json()
        name = data.get('name')
        age = data.get('age')
        address = data.get('address')

        query = ModelDatabase.query.get(id)
        query.name = name
        query.age = age
        query.address = address
        db.session.commit()

        return {
            "status":200,
            "message":"success"
        }, 200
    
    def delete(self, id):
        query = ModelDatabase.query.get(id)
        db.session.delete(query)
        db.session.commit()

        return {
            "status":200,
            "message":"success"
        }, 200


# inisiasi url/api
api.add_resource(ExampleResource, "/api/users", methods=["GET", "POST", "DELETE"])
api.add_resource(UpdateResource, "/api/users/<id>", methods=["GET", "PUT", "DELETE"])

if __name__ == "__main__":
    app.run(debug=True, port=5005)
