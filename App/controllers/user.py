from App.models import User
#from App.models import StaffUser, AdminUser
from App.models import UserFactory
# from App.database import db

# Creates a new user given their username, password and access level
def create_user(username, password):
    new_user = UserFactory()
    user = new_user.getUser("User", username=username, password=password)
    user.add()
    user.commit()
    #db.session.add(new_user)
    #db.session.commit()
    return user

# Creates a new user given their username, password and access level
def create_staffuser(username, password):
    new_user = UserFactory()
    staff_user = new_user.getUser("Staff", username=username, password=password)
    staff_user.add()
    staff_user.commit()
    #db.session.add(new_user)
    #db.session.commit()
    return staff_user

# Creates a new user given their username, password and access level
def create_adminuser(username, password):
    new_user = UserFactory()
    admin_user = new_user.getUser("Admin", username=username, password=password)
    admin_user.add()
    admin_user.commit()
    #db.session.add(new_user)
    #db.session.commit()
    return admin_user


# Gets a user by their username
def get_user_by_username(username):
    return User.query.filter_by(username=username).first()


# Gets a user by their id
def get_user(id):
    return User.query.get(id)


# Gets all users that have a certain access level
def get_users_by_access(access):
    return User.query.filter_by(access=access).all()


# Gets all users in the database
def get_all_users():
    return User.query.all()


# Gets all users and returns them as a JSON object
def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    return [user.to_json() for user in users]


# Updates a user's username given their id and username
def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        user.add()
        return user.commit()
        #db.session.add(user)
        #return db.session.commit()
    return None


# Deletes a user given their id
def delete_user(id):
    user = get_user(id)
    if user:
        user.delete()
        return user.commit()
        #db.session.delete(user)
        #return db.session.commit()
    return None
