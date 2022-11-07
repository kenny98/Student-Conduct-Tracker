from flask import Blueprint, jsonify, request
from flask_jwt import jwt_required, current_identity

from App.controllers import (
    create_review,
    get_review,
    get_all_reviews,
    update_review,
    delete_review,
)

review_views = Blueprint("review_views", __name__, template_folder="../templates")


# Function to allow only staff members to make review requests
def permit_staff():
    if (current_identity.is_staff()):
        return True
    else: return False

# Create review given user id, student id and text
@review_views.route("/api/reviews", methods=["POST"])
@jwt_required()
def create_review_action():
    if (permit_staff()):
        data = request.json
        review = create_review(
            user_id=data["user_id"], student_id=data["student_id"], text=data["text"]
        )
        if review:
            return jsonify(review.to_json()), 201
        return jsonify({"error": "review not created"}), 400
    else:
        return jsonify({"message": "Access denied"}), 403


# List all reviews
@review_views.route("/api/reviews", methods=["GET"])
@jwt_required()
def get_all_reviews_action():
    if (permit_staff()):
        reviews = get_all_reviews()
        return jsonify([review.to_json() for review in reviews]), 200
    else:
        return jsonify({"message": "Access denied"}), 403


# Gets review given review id
@review_views.route("/api/reviews/<int:review_id>", methods=["GET"])
@jwt_required()
def get_review_action(review_id):
    if (permit_staff()):
        review = get_review(review_id)
        if review:
            return jsonify(review.to_json()), 200
        return jsonify({"error": "review not found"}), 404
    else:
        return jsonify({"message": "Access denied"}), 403


# Upvotes post given post id and user id
@review_views.route("/api/reviews/<int:review_id>/upvote", methods=["PUT"])
@jwt_required()
def upvote_review_action(review_id):
    if (permit_staff()):
        review = get_review(review_id)
        if review:
            review.vote(current_identity.id, "up")
            return jsonify(review.to_json()), 200
        return jsonify({"error": "review not found"}), 404
    else:
        return jsonify({"message": "Access denied"}), 403


# Downvotes post given post id and user id
@review_views.route("/api/reviews/<int:review_id>/downvote", methods=["PUT"])
@jwt_required()
def downvote_review_action(review_id):
    if (permit_staff()):
        review = get_review(review_id)
        if review:
            review.vote(current_identity.id, "down")
            return jsonify(review.to_json()), 200
        return jsonify({"error": "review not found"}), 404
    else:
        return jsonify({"message": "Access denied"}), 403


# Updates post given post id and new text
# Only admins or the original reviewer can edit a review
@review_views.route("/api/reviews/<int:review_id>", methods=["PUT"])
@jwt_required()
def update_review_action(review_id):
    data = request.json
    review = get_review(review_id)
    if review:
        if current_identity.id == review.user_id or current_identity.is_admin():
            update_review(review_id, text=data["text"])
            return jsonify({"message": "post updated successfully"}), 200
        else:
            return jsonify({"error": "Access denied"}), 403
    return jsonify({"error": "review not found"}), 404


# Deletes post given post id
# Only admins or the original reviewer can delete a review
@review_views.route("/api/reviews/<int:review_id>", methods=["DELETE"])
@jwt_required()
def delete_review_action(review_id):
    review = get_review(review_id)
    if review:
        if current_identity.id == review.user_id or current_identity.is_admin():
            delete_review(review_id)
            return jsonify({"message": "post deleted successfully"}), 200
        else:
            return jsonify({"error": "Access denied"}), 403
    return jsonify({"error": "review not found"}), 404


# Gets all votes for a given review
@review_views.route("/api/reviews/<int:review_id>/votes", methods=["GET"])
@jwt_required()
def get_review_votes_action(review_id):
    if (permit_staff()):
        review = get_review(review_id)
        if review:
            return jsonify(review.get_all_votes()), 200
        return jsonify({"error": "review not found"}), 404
    else:
        return jsonify({"message": "Access denied"}), 403