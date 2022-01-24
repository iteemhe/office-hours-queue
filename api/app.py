from flask import Flask
from flask_restful import Resource, Api
from flask_jwt import JWT

from security import authenticate, identity

"""
Driver program for the RESTful CRUD API
@author Jiahao He
@version 1/24/2022
"""

app = Flask(__name__)
app.secret_key = "a very strong password"
api = Api(app)

jwt = JWT(app, authenticate, identity)

if __name__ == "__main__":
    app.run(port=8888, debug=True)
