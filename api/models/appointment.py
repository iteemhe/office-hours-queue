from db import db


class AppointmentModel(db.Model):
    __tablename__ = "appointments"
    id = db.Column(db.Integer, primary_key=True)
    unique_name = db.Column(db.String)
    course = db.Column(db.String)
    location = db.Column(db.String)

    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"))

    def __init__(self, unique_name, course, location):
        """
        Constructor for AppointmentModel
        """
        self.unique_name = unique_name
        self.course = course
        self.location = location

    def json(self):
        """
        Helper method to return a JSON
        """
        return {
            "unique_name": self.unique_name,
            "course": self.course,
            "location": self.location,
        }

    @classmethod
    def find_by_unique_name(cls, unique_name, course):
        """
        Lookup appointment by course and unique_name
        """
        return (
            cls.query.filter_by(unique_name=unique_name)
            .filer_by(course=course)
            .first()
        )

    @classmethod
    def find_by_id(cls, _id):
        """
        Lookup appointment by id
        """
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_course(cls, course):
        """
        Lookup appointment by course name
        """
        return cls.query.filter_by(course=course)

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
