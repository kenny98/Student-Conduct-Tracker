# Refactor Item 1 - Model for Staff
from App.models import User
from App.database import db

class StaffUser(User):
    reviews = db.relationship(
        "Review", backref="user", lazy=True, cascade="all, delete-orphan"
    )

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)
        self.access = 1