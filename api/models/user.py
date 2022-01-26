from db import db


class UserModel(db.Model):
    """
    Configurations for SQL
    """

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    unique_name = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    is_admin = db.Column(db.Boolean, default=False)

    # Not safe but convenient for testing
    # Replace with OAth later
    password = db.Column(db.String)

    def __init__(
        self, unique_name, first_name, last_name, is_admin, password
    ):
        """
        Constructor for UserModel class
        """

        self.unique_name = unique_name
        self.first_name = first_name
        self.last_name = last_name
        self.is_admin = is_admin
        self.password = password

    def json(self):
        """
        Helper method to return the user object in JSON
        """

        return {
            "unique_name": self.unique_name,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "is_admin": self.is_admin,
            "user_id": self.id,
        }

    @classmethod
    def find_by_unique_name(cls, unique_name):
        """
        Lookup users by its unique_name
        """

        return cls.query.filter_by(unique_name=unique_name).first()

    @classmethod
    def find_by_id(cls, _id):
        """
        Lookup users by id
        """

        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        """
        Update or insert the user to the database
        """

        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """
        Remove the user from the database
        """

        db.session.delete(self)
        db.session.commit()
