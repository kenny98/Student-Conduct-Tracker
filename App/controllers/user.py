from App.models import User
# from App.database import db


# Creates a new user given their username, password and access level
def create_user(username, password, access=1):
    new_user = User(username=username, password=password, access=access)
    new_user.add()
    new_user.commit()
    #db.session.add(new_user)
    #db.session.commit()
    return new_user


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
