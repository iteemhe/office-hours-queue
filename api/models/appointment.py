from db import db

"""
For handleing all stuff about appointments
"""


class AppointmentModel(db.Model):
    # Table name
    __tablename__ = "appointments"

    # Table for Appointment
    id = db.Column(db.Integer, primary_key=True)
    unique_name = db.Column(db.String)
    course_name = db.Column(db.String)
    location = db.Column(db.String)

    # Connect to CourseModel
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"))
    course = db.relationship("CourseModel")

    def __init__(self, unique_name, course_name, location, course_id):
        """
        Constructor for AppointmentModel
        """

        self.unique_name = unique_name
        self.course_name = course_name
        self.location = location
        # Optional, and not enforced by sqlite
        self.course_id = course_id

    def json(self):
        """
        Helper method to return a JSON
        """

        return {
            "unique_name": self.unique_name,
            "course_name": self.course_name,
            "location": self.location,
            # for identify position in queue
            "appointment_id": self.id,
            # return course_id for completeness of API
            "course_id": self.course_id,
        }

    @classmethod
    def find_by_unique_name_course(cls, unique_name, course_name):
        """
        Lookup appointment by course and unique_name
        """

        return cls.query.filter_by(
            unique_name=unique_name, course_name=course_name
        ).first()

    @classmethod
    def find_by_id(cls, _id):
        """
        Lookup appointment by id
        """

        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_course(cls, course_name):
        """
        Lookup appointment by course name
        """

        return cls.query.filter_by(course_name=course_name)

    @classmethod
    def find_all(cls):
        """
        Return all appointments
        """
        return cls.query.all()

    def save_to_db(self):
        """
        Add or update appointment
        """
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """
        Remove appointment from db
        """
        db.session.delete(self)
        db.session.commit()
