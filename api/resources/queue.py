from models.queue import QueueModel
from flask_restful import Resource


class Queue(Resource):
    def get(self, course):
        return QueueModel.find_all_appointments(course)
