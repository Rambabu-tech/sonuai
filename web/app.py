import os
import json
import sys

from redis import Redis
from rq import Queue

from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from extensions import db
from web.models import User

# ✅ FIX PATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ✅ REDIS
redis_conn = Redis()
queue = Queue("jobs", connection=redis_conn)

# ✅ FLASK APP
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "secret")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# 🚀 DASHBOARD
@app.route("/")
@login_required
def dashboard():

    file = f"applications_{current_user.id}.json"

    jobs = []
    if os.path.exists(file):
        try:
            with open(file) as f:
                jobs = json.load(f)
        except:
            jobs = []

    return render_template("dashboard.html", jobs=jobs)


# 🚀 RUN JOBS (FIXED)
@app.route("/run")
@login_required
def run_jobs():

    # ✅ IMPORT INSIDE (fix circular import)
    from worker_tasks import process_user_jobs

    # ❌ REMOVE subprocess → VERY IMPORTANT
    # subprocess.Popen(["python", "main.py", str(current_user.id)])

    # ✅ ONLY QUEUE
    queue.enqueue(process_user_jobs, current_user.id)

    return "🚀 Job started in background!"


# 🚀 UPLOAD RESUME
@app.route("/upload", methods=["POST"])
@login_required
def upload():

    file = request.files["resume"]

    if not file:
        return redirect("/")

    os.makedirs("uploads", exist_ok=True)

    path = os.path.join("uploads", secure_filename(file.filename))
    file.save(path)

    current_user.resume_path = path
    db.session.commit()

    return redirect("/")


# 🚀 LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        user = User.query.filter_by(email=request.form["email"]).first()

        if user and check_password_hash(user.password_hash, request.form["password"]):
            login_user(user)
            return redirect("/")

    return render_template("login.html")


# 🚀 REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        user = User(
            email=request.form["email"],
            password_hash=generate_password_hash(request.form["password"])
        )
        db.session.add(user)
        db.session.commit()

        return redirect("/login")

    return render_template("register.html")


# 🚀 LOGOUT
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")


# 🚀 RUN SERVER
if __name__ == "__main__":
    app.run(debug=True)