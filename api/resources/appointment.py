from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.appointment import AppointmentModel


class Appointment(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument(
        "unique_name",
        type=str,
        required=True,
        help="This field cannot be empty",
    )
    parse.add_argument(
        "course",
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

    def get(self):
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
        if AppointmentModel.query.filter_by(
            unique_name=data["unique_name"], course=data["course"]
        ).first():
            return {
                "message": "You can only schedule one appointment in the same course"
            }, 400

        appointment = AppointmentModel(**data)
        appointment.save_to_db()
        return {"message": "Appointment scheduled successfully"}

    @jwt_required()
    def put(self):
        data = Appointment.parse.parse_args()
        appointment = AppointmentModel.query.filter(
            unique_name=data["unique_name"], course=data["course"]
        ).first()

        if appointment:
            appointment.location = data["location"]
        else:
            appointment = AppointmentModel(**data)

        appointment.save_to_db()
        return {"message": "Appointment change saved successfully"}
