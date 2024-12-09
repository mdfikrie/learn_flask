# Import library
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS

# Inisiasi object flask
app = Flask(__name__)

# Inisiasi object flask_restful
api = Api(app)

# Inisiasi variable kosong 
identitas = {}

# Inisiasi object CORS
CORS(app)

# membuat class resource
class ExampleResource(Resource):
    # metode get dan post
    def get(self):
        return {
            "message":"success",
            "data":identitas
        };

    def post(self):
        if(request.is_json):
            data = request.get_json()
            name = data.get('name')
            age = data.get('age')
        else:
            name = request.form['name']
            age = request.form['age']
        
        identitas['name'] = name
        identitas['age'] = age
        
        response = {"message":"success"}
        return response


# setup resource
api.add_resource(ExampleResource, "/api", methods=["GET","POST"])

if __name__ == "__main__":
    app.run(debug=True, port=5005)