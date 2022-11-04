from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from abc import ABC, abstractmethod

# Maybe use interface here, so that it can be implemented by children (Staff and Admin)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    access = db.Column(db.Integer, nullable=False)

    @abstractmethod
    def __init__(self, username, password, access=1):
        self.username = username
        self.set_password(password)
        self.access = access

    @abstractmethod
    def is_admin(self):
        return self.access == 2

    def allowed(self, access_level):
        return self.access >= access_level

    def to_json(self):
        return {"id": self.id, "username": self.username, "access": self.access}

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method="sha256")

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
    
    # Refactor Item 1 - Only Model should interact with Database
    def add(self):
        db.session.add(self)
    
    def commit(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)