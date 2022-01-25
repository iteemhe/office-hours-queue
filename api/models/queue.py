from models.appointment import AppointmentModel


class QueueModel:
    def __init__(self, course):
        pass

    @classmethod
    def find_all_appointments(cls, course):
        return AppointmentModel.find_by_course(course)
