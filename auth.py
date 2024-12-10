import jwt
from flask import Flask, request, make_response, jsonify
from flask_restful import Resource, Api
import datetime
from functools import wrap

# inisiasi flask
app = Flask(__name__)
api = Api(app)

class LoginUser(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        return "halo";

api.add_resource(LoginUser, "/api/login", methods=["POST"])

if __name__ == "__main__":
    app.run(debug=True, port=5050)
