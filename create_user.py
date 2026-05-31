from web.app import app
from extensions import db
from web.models import User
from werkzeug.security import generate_password_hash

with app.app_context():

    user = User(
        email="rambabukurva899@gmail.com",
        password_hash=generate_password_hash("test123"),
        resume_path="resume/resume.txt"
    )

    db.session.add(user)
    db.session.commit()

    print("User created with ID:", user.id)