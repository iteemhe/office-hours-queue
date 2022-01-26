from db import db
from app import app

"""
Run Flask API in Heroku env
"""

db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


# if __name__ == "__main__":

# app.run(port=5000, debug=True)
