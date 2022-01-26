from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.appointment import AppointmentModel

from models.course import CourseModel


class Course(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument(
        "course_name",
        type=str,
        required=True,
        help="This field cannot be empty!",
    )
    parse.add_argument(
        "is_open",
        type=bool,
        required=True,
        help="This field cannot be empty",
    )

    def get(self, course_name):
        course = CourseModel.find_by_course_name(course_name)
        if course:
            return course.json()
        return {"message": "Course cannot found"}

    @jwt_required()
    def post(self, course_name):
        data = Course.parse.parse_args()
        if course_name != data["course_name"]:
            return {"message": "Request course_name must match"}
        if CourseModel.find_by_course_name(course_name):
            return {"message": "Course already exists."}
        course = CourseModel(**data)
        course.save_to_db()
        return {"message": "Course created successfully."}

    @jwt_required()
    def put(self, course_name):
        data = Course.parse.parse_args()
        if course_name != data["course_name"]:
            return {"message": "Request course_name must match"}
        course = CourseModel.find_by_course_name(course_name)
        if course:
            # Only allow to change course_name
            course.course_name = data["course_name"]
        else:
            course = CourseModel(**data)
        course.save_to_db()
        return {"message": "Course changed successfully"}

    @jwt_required()
    def delete(self, course_name):
        course = CourseModel.find_by_course_name(course_name)

        if course:
            course.delete_from_db()

        return {"message": "Course deleted successfully"}


class CourseList(Resource):
    def get(self):
        courses = CourseModel.find_all()
        if courses:
            return {"courses": [c.json() for c in courses]}
        return {"courses": []}


class CourseQueue(Resource):
    def get(self, course_name):
        course = CourseModel.find_by_course_name(course_name)
        if course is None:
            return {"message": "Course not found, queue does not exist"}

        queue = AppointmentModel.find_by_course(course_name)

        if queue:
            return {
                "course_name": course_name,
                "appointments": [a.json() for a in queue],
            }

        return {"course_name": course_name, "appointments": []}
