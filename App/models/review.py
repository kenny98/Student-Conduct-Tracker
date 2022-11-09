from App.database import db
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.mutable import MutableDict, MutableList
from sqlalchemy import PickleType


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    text = db.Column(db.String(1000), nullable=False)
    votes = db.Column(MutableDict.as_mutable(JSON), nullable=False)
    # list of review voters - used to tracks who voted already
    voters = db.Column(MutableList.as_mutable(PickleType),
                                    default=[])
    def __init__(self, user_id, student_id, text):
        self.user_id = user_id
        self.student_id = student_id
        self.text = text
        self.votes = {"num_upvotes": 0, "num_downvotes": 0}
        self.voters = []

    def vote(self, user_id, vote):
        self.votes.update({user_id: vote})
        self.voters.append(user_id)
        """ self.votes.update(
            {"num_upvotes": len([vote for vote in self.votes.values() if vote == "up"])}
        )
        self.votes.update(
            {
                "num_downvotes": len(
                    [vote for vote in self.votes.values() if vote == "down"]
                )
            }
        ) """

        if (vote == "up" ):
            self.votes["num_upvotes"] += 1

        if (vote == "down"):
            self.votes["num_downvotes"] += 1

    def get_voters(self):
        return self.voters

    def get_num_upvotes(self):
        return self.votes["num_upvotes"]

    def get_num_downvotes(self):
        return self.votes["num_downvotes"]

    def get_karma(self):
        return self.get_num_upvotes() - self.get_num_downvotes()

    def get_all_votes(self):
        return self.votes

    def to_json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "student_id": self.student_id,
            "text": self.text,
            "karma": self.get_karma(),
            "num_upvotes": self.get_num_upvotes(),
            "num_downvotes": self.get_num_downvotes(),
        }
    
    # Refactor Item 1 - Only Model should interact with Database
    def add(self):
        db.session.add(self)
    
    def commit(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
