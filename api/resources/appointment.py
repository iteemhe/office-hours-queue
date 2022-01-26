from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.appointment import AppointmentModel
from models.course import CourseModel


class Appointment(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument(
        "unique_name",
        type=str,
        required=True,
        help="This field cannot be empty",
    )
    parse.add_argument(
        "course_name",
        type=str,
        required=True,
        help="This field cannot be empty",
    )
    parse.add_argument(
        "location",
        type=str,
        required=True,
        help="This field cannot be empty",
    )
    parse.add_argument(
        "course_id",
        type=int,
        required=True,
        help="This field cannot be empty",
    )

    def get(self):
        """
        Return a list of appointments
        """

        return {
            "appointments": [
                list(
                    map(
                        lambda x: x.json(), AppointmentModel.query.all()
                    )
                )
            ]
        }

    @jwt_required()
    def post(self):
        data = Appointment.parse.parse_args()

        # find if an appointment already exists
        if AppointmentModel.find_by_unique_name_course(
            data["unique_name"], data["course_name"]
        ):
            return {
                "message": "You can only schedule one appointment in the same course"
            }, 400
        elif (
            CourseModel.find_by_course_name(data["course_name"]) is None
        ):
            return {"message": "Course does not exist"}

        # Create an appointment and save to database
        appointment = AppointmentModel(**data)
        appointment.save_to_db()
        return {"message": "Appointment scheduled successfully"}

    @jwt_required()
    def put(self):
        data = Appointment.parse.parse_args()

        # find if the appointment already exists
        appointment = AppointmentModel.find_by_unique_name_course(
            data["unique_name"], data["course_name"]
        )

        if appointment:
            # only permit to change the location
            appointment.location = data["location"]
        else:
            appointment = AppointmentModel(**data)

        appointment.save_to_db()
        return {"message": "Appointment change saved successfully"}

    @jwt_required()
    def delete(self):
        data = Appointment.parse.parse_args()

        appointment = AppointmentModel.find_by_unique_name_course(
            data["unique_name"], data["course_name"]
        )

        if appointment:
            appointment.delete_from_db()

        return {"message": "Appointment cancelled successfully"}
