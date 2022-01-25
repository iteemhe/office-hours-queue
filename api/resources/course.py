from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

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
        course = CourseModel.query.filter_by(
            course_name=course_name
        ).first()

        if course:
            return course.json()
        return {"message": "Course cannot found"}

    @jwt_required()
    def post(self, course_name):
        data = Course.parse.parse_args()
        if CourseModel.query.filter_by(course_name=course_name):
            return {"message": "Course already exists."}
        course = CourseModel(**data)
        course.save_to_db()
        return {"message": "Course created successfully."}

    @jwt_required()
    def put(self, course_name):
        data = Course.parse.parse_args()
        course = CourseModel.query.filter_by(course_name=course_name)
        if course:
            course.course_name = data["course_name"]
        else:
            course = CourseModel(*data)
        course.save_to_db()
        return {"message": "Course changed successfully"}

    @jwt_required()
    def delete(self, course_name):
        course = CourseModel.query.filter_by(
            course_name=course_name
        ).first()
        if course:
            course.delete_from_db()
        return {"message": "Course deleted successfully"}


class CourseList(Resource):
    def get(self):
        courses = CourseModel.query.all()
        if courses:
            return {"courses": [list(map(lambda x: x.json(), courses))]}
        return {"courses": []}
