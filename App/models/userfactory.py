from App.models import User, StaffUser, AdminUser

class UserFactory:
    def getUser(self, usertype, username, password) -> User:
        if (usertype == "Staff"):
            return StaffUser(username=username, password=password)
        if (usertype == "Admin"):
            return AdminUser(username=username, password=password)
        if (usertype == "User"):
            return StaffUser(username=username, password=password)
        return None