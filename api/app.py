import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from resources.course import Course, CourseList, CourseQueue
from resources.user import User, UserRegister
from resources.appointment import Appointment

from security import authenticate, identity  # functions for JWT

"""
Driver program for the RESTful CRUD API
@author Jiahao He
@version 1/24/2022
"""


app = Flask(__name__)

# Preparation to deploy to Heroku
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL",  # Heroku env
    "sqlite:///data.db",  # default path for local test
).replace("postgres", "postgresql")

# SQL performance
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# For JWT reports appropriate response code
app.config["PROPGATE_EXCEPTIONS"] = True
app.secret_key = "a very strong key"
api = Api(app)

# @app.before_first_request
# def create_tables():
#     db.create_all()

jwt = JWT(app, authenticate, identity)  # /auth endpoint

# CRUD for user, and regisration
api.add_resource(User, "/user/<string:unique_name>")
api.add_resource(UserRegister, "/register")


# CRUD for appointments
api.add_resource(Appointment, "/appointment")

# CRUD for courses
api.add_resource(Course, "/course/<string:course_name>")
api.add_resource(CourseQueue, "/course/<string:course_name>/queue")
api.add_resource(CourseList, "/courses")

# if __name__ == "__main__":
#     db.init_app(app)
#     app.run(port=5000, debug=True)
