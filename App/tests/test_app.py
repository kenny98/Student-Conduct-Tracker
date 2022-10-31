import pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import create_db
from App.models import User, Student, Review
from App.controllers import (
    create_user,
    get_all_users_json,
    authenticate,
    get_user,
    get_user_by_username,
    update_user,
    delete_user,
)

from wsgi import app


LOGGER = logging.getLogger(__name__)

"""
   Unit Tests
"""


class UserUnitTests(unittest.TestCase):
    def test_new_user(self):
        user = User("bob", "bobpass")
        assert user.username == "bob"
    
    def test_new_admin_user(self):
        user = User("bob", "bobpass", 2)
        assert user.access == 2

    def test_new_normal_user(self):
        user = User("bob", "bobpass", 1)
        assert user.access == 1    

    def test_user_is_admin(self):
        user = User("bob", "bobpass", 2)
        assert user.is_admin()

    def test_user_is_not_admin(self):
        user = User("bob", "bobpass", 1)
        assert not user.is_admin()

    # pure function no side effects or integrations called
    def test_to_json(self):
        user = User("bob", "bobpass")
        user_json = user.to_json()
        self.assertDictEqual(user_json, {"access":1, "id": None, "username": "bob"})

    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method="sha256")
        user = User("bob", password)
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob", password)
        assert user.check_password(password)

class StudentUnitTests(unittest.TestCase):
    def test_new_student(self):
        student = Student("bob","FST", "Computer Science")
        assert student.name == "bob" and student.faculty == "FST" and student.programme == "Computer Science"

    def test_student_to_json(self):
        student = Student("bob","FST", "Computer Science")
        student_json = student.to_json()
        self.assertDictEqual(student_json, {"faculty": "FST", "id": None, "karma": 0, "name": "bob", "programme": "Computer Science"})

    def test_student_karma(self):
        with self.subTest("No reviews"):
            student = Student("bob","FST", "Computer Science")
            self.assertEqual(student.get_karma(), 0)

        with self.subTest("No reviews"):
            student = Student("bob","FST", "Computer Science")
            mockReview = Review(1, 1, "good")
            mockReview.vote(1, "up")
            student.reviews.append(mockReview)
            self.assertEqual(student.get_karma(), 1)

        with self.subTest("One negative review"):
            student = Student("bob","FST", "Computer Science")
            mockReview1 = Review(1, 1, "good")
            mockReview1.vote(1, "down")
            student.reviews.append(mockReview1)
            self.assertEqual(student.get_karma(), -1)

class ReviewUnitTests(unittest.TestCase):
    def test_new_review(self):
        review = Review(1, 1, "good")
        assert review.student_id == 1 and review.user_id == 1 and review.text == "good"

    def test_review_to_json(self):
        review = Review(1, 1, "good")
        review_json = review.to_json()
        self.assertDictEqual(review_json, {
            "id": None,
            "user_id": 1,
            "student_id":1,
            "text": "good",
            "karma": 0,
            "num_upvotes": 0,
            "num_downvotes": 0,
        })

    def test_review_vote(self):
        with self.subTest("Upvote"):
            review = Review(1, 1, "good")
            review.vote(1, "up")
            self.assertEqual(review.votes['num_upvotes'], 1)
        
        with self.subTest("Downvote"):
            review = Review(1, 1, "good")
            review.vote(1, "down")
            self.assertEqual(review.votes['num_downvotes'], 1)

    def test_review_get_num_upvotes(self):
        with self.subTest("No votes"):
            review = Review(1, 1, "good")
            self.assertEqual(review.get_num_upvotes(), 0)

        with self.subTest("One upvote"):
            review = Review(1, 1, "good")
            review.vote(1, "up")
            self.assertEqual(review.get_num_upvotes(), 1)
        
        with self.subTest("One downvote"):
            review = Review(1, 1, "good")
            review.vote(1, "down")
            self.assertEqual(review.get_num_upvotes(), 0)

    def test_review_get_num_downvotes(self):
        with self.subTest("No votes"):
            review = Review(1, 1, "good")
            self.assertEqual(review.get_num_downvotes(), 0)

        with self.subTest("One upvote"):
            review = Review(1, 1, "good")
            review.vote(1, "up")
            self.assertEqual(review.get_num_downvotes(), 0)
        
        with self.subTest("One downvote"):
            review = Review(1, 1, "good")
            review.vote(1, "down")
            self.assertEqual(review.get_num_downvotes(), 1)
    
    def test_review_get_karma(self):
        with self.subTest("No votes"):
            review = Review(1, 1, "good")
            self.assertEqual(review.get_karma(), 0)

        with self.subTest("One upvote"):
            review = Review(1, 1, "good")
            review.vote(1, "up")
            self.assertEqual(review.get_karma(), 1)
        
        with self.subTest("One downvote"):
            review = Review(1, 1, "good")
            review.vote(1, "down")
            self.assertEqual(review.get_karma(), -1)

    def test_review_get_all_votes(self):
        with self.subTest("No votes"):
            review = Review(1, 1, "good")
            self.assertEqual(review.get_all_votes(), {"num_upvotes": 0, "num_downvotes": 0})

        with self.subTest("One upvote"):
            review = Review(1, 1, "good")
            review.vote(1, "up")
            self.assertEqual(review.get_all_votes(), {1:"up","num_upvotes": 1, "num_downvotes": 0})
        
        with self.subTest("One downvote"):
            review = Review(1, 1, "good")
            review.vote(1, "down")
            self.assertEqual(review.get_all_votes(), {1:"down", "num_upvotes": 0, "num_downvotes": 1})
        
        with self.subTest("One upvote and one downvote"):
            review = Review(1, 1, "good")
            review.vote(1, "up")
            review.vote(2, "down")
            self.assertEqual(review.get_all_votes(), {1:"up", 2:"down", "num_upvotes": 1, "num_downvotes": 1})
    

"""
    Integration Tests
"""

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app.config.update({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///test.db"})
    create_db(app)
    yield app.test_client()
    # os.unlink(os.getcwd() + "/App/test.db")


def test_authenticate():
    user = create_user("bob", "bobpass")
    assert authenticate("bob", "bobpass") != None



class UsersIntegrationTests(unittest.TestCase):
    def test_create_admin(self):
        admin = create_user("rick", "rickpass", 2)
        assert admin.access == 2

    # def test_get_all_users_json(self):
    #     users_json = get_all_users_json()
    #     self.assertListEqual(
    #         [{"access":1,"id": 1, "username": "bob"}, {"access":2,"id": 2, "username": "rick"}], users_json
    #     )
    def test_create_user(self):
        user = create_user("john", "johnpass", 1)
        assert user.username == "john"
    # Tests data changes in the database

    # def test_update_user(self):
    #     update_user(1, "ronnie")
    #     user = get_user(1)
    #     assert user.username == "ronnie"

    # def test_delete_user(self):
    #     user = create_user("bobby", "bobbypass", 1)
    #     delete_user(3)
    #     assert get_user(3) == None

# class UsersIntegrationSuite(unittest.TestSuite):
#     UsersIntegrationSuite = unittest.TestLoader().loadTestsFromTestCase(UsersIntegrationTests)
#     runner = unittest.TextTestRunner()
#     runner.run(UsersIntegrationSuite)


