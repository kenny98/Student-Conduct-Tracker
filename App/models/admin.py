# Refactor Item 1 - Model for Admin
from App.models import User

class AdminUser(User):
    def __init__(self, username, password, access=2):
        self.username = username
        self.set_password(password)
        self.access = access