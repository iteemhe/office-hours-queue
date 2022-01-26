from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.user import UserModel


class User(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument(
        "unique_name",
        type=str,
        required=True,
        help="This field cannot be empty!",
    )
    parse.add_argument(
        "first_name",
        type=str,
        required=True,
        help="This field cannot be empty",
    )
    parse.add_argument(
        "last_name",
        type=str,
        required=True,
        help="This field cannot be empty",
    )
    parse.add_argument(
        "is_admin",
        type=bool,
        required=True,
        help="This field cannot be empty",
    )
    parse.add_argument(
        "password",
        type=str,
        required=True,
        help="This field cannot be empty",
    )

    @jwt_required()
    def get(self, unique_name):
        user = UserModel.find_by_unique_name(unique_name)
        if user:
            return user.json()
        return {"message": "User not found."}

    @jwt_required()
    def delete(self, unique_name):
        user = UserModel.find_by_unique_name(unique_name)
        if user:
            user.delete_from_db()
        return {"message": "User deleted."}, 200

    @jwt_required()
    def put(self, unique_name):
        data = User.parse.parse_args()
        user = UserModel.find_by_unique_name(unique_name)
        if user:
            if user.password != data["password"]:
                return {"message": "Password does not match"}

            user.name = data["name"]
            user.first_name = data["first_name"]
            user.last_name = data["last_name"]
            user.is_admin = data["is_admin"]
            user.save_to_db()
        else:
            return {"message": "Please register first"}
        return user.json(), 202


class UserRegister(Resource):
    """
    Handle new users register
    """

    parse = reqparse.RequestParser()
    parse.add_argument(
        "unique_name",
        type=str,
        required=True,
        help="This field cannot be empty!",
    )
    parse.add_argument(
        "first_name",
        type=str,
        required=True,
        help="This field cannot be empty",
    )
    parse.add_argument(
        "last_name",
        type=str,
        required=True,
        help="This field cannot be empty",
    )
    parse.add_argument(
        "is_admin",
        type=bool,
        required=True,
        help="This field cannot be empty",
    )
    parse.add_argument(
        "password",
        type=str,
        required=True,
        help="This field cannot be empty",
    )

    def post(self):
        data = UserRegister.parse.parse_args()
        if UserModel.find_by_unique_name(data["unique_name"]):
            return {"message": "User already exists"}

        # user = UserModel(
        #     data["unique_name"],
        #     data["name"],
        #     data["first_name"],
        #     data["is_admin"],
        #     data["password"],
        # )
        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully"}, 202
