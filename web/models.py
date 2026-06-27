from extensions import db
from flask_login import UserMixin
from datetime import datetime


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password_hash = db.Column(db.String(255), nullable=False)

    resume_path = db.Column(db.String(255))

    # 🔥 RELATIONSHIP (VERY IMPORTANT)
    applications = db.relationship(
        "JobApplication",
        backref="user",
        lazy=True
    )


class JobApplication(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    job_title = db.Column(db.String(255))
    company = db.Column(db.String(255))
    job_url = db.Column(db.String(500))

    score = db.Column(db.Float)

    decision = db.Column(db.String(50))

    # ✅ STATUS SYSTEM
    status = db.Column(db.String(50), default="MATCHED")

    # ✅ AI OUTPUT
    cover_letter = db.Column(db.Text)

    # ✅ SOURCE
    source = db.Column(db.String(100), default="unknown")

    # 🔥 NEW (VERY IMPORTANT)
    skill_matches = db.Column(db.Integer, default=0)
    role_match = db.Column(db.Boolean, default=False)

    # 🔥 TIMESTAMP
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )