from db import db


class CourseModel(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String)
    is_open = db.Column(db.Boolean, default=False)

    appointments = db.relationship(
        "AppointmentModel", lazy="dynamic"  # improve performance
    )

    def __init__(self, course_name, is_open):
        self.course_name = course_name
        self.is_open = is_open

    def json(self):
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
        }

    @classmethod
    def find_by_course_name(cls, course_name):
        return cls.query.filter_by(course_name=course_name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
