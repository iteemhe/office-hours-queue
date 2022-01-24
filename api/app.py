from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import User, UserRegister
from db import db

"""
Driver program for the RESTful CRUD API
@author Jiahao He
@version 1/24/2022
"""


def main():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = "a very strong password"
    api = Api(app)
    jwt = JWT(app, authenticate, identity)  # /auth endpoint

    api.add_resource(User, "/user/<string:unique_name>")
    api.add_resource(UserRegister, "/register")

    db.init_app(app)
    app.run(port=5000, debug=True)
    return


if __name__ == "__main__":
    main()
