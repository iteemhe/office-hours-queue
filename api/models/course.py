from db import db


class CourseModel(db.Model):
    # Table name
    __tablename__ = "courses"

    # Tables for CourseModel
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String)
    is_open = db.Column(db.Boolean, default=False)

    # Connect to AppointmentModel
    appointments = db.relationship(
        "AppointmentModel", lazy="dynamic"  # improve performance
    )

    def __init__(self, course_name, is_open):
        """
        Constructor for CourseModel
        """

        self.course_name = course_name
        self.is_open = is_open

    def json(self):
        """
        Helper function to return a JSON
        """

        return {
            "course_name": self.course_name,
            "is_open": self.is_open,
            "appointments": [
                list(
                    map(
                        lambda x: x.json(),
                        self.appointments.all(),
                        # appointments is a query now, not an object
                    )
                )
            ],
            "course_id": self.id,
        }

    @classmethod
    def find_by_course_name(cls, course_name):
        return cls.query.filter_by(course_name=course_name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
