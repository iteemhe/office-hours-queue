from werkzeug.security import safe_str_cmp
from models.user import UserModel


def authenticate(unique_name, password):
    user = UserModel.find_by_unique_name(unique_name)
    # print(unique_name)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload["identity"]
    # print(user_id)
    return UserModel.find_by_id(user_id)
