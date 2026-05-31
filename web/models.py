from extensions import db
from flask_login import UserMixin


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password_hash = db.Column(db.String(255), nullable=False)

    resume_path = db.Column(db.String(255))


class JobApplication(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    job_title = db.Column(db.String(255))

    job_url = db.Column(db.String(500))

    company = db.Column(db.String(255))

    score = db.Column(db.Float)

    decision = db.Column(db.String(50))

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )