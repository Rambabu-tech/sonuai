import os
import sys

from flask import Flask, render_template, redirect, request, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from extensions import db
from web.models import User, JobApplication

# PATH FIX
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "supersecret")

# ===============================
# DATABASE CONFIG
# ===============================
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
db_path = os.path.join(BASE_DIR, "instance", "site.db")

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# ===============================
# LOGIN CONFIG
# ===============================
login_manager = LoginManager(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# ===============================
# DASHBOARD
# ===============================
@app.route("/")
@login_required
def dashboard():

    status_filter = request.args.get("status")

    query = JobApplication.query.filter_by(user_id=current_user.id)

    if status_filter:
        query = query.filter_by(status=status_filter)

    jobs = query.order_by(JobApplication.created_at.desc()).all()

    return render_template("dashboard.html", jobs=jobs)


# ===============================
# RUN AI (MATCH JOBS)
# ===============================
@app.route("/run")
@login_required
def run_jobs():

    from main import run_for_user

    run_for_user(current_user.id)

    return jsonify({"status": "started"})


# ===============================
# RETRY FAILED JOB
# ===============================
@app.route("/retry/<int:job_id>")
@login_required
def retry_job(job_id):

    job = JobApplication.query.get(job_id)

    if not job:
        return "Job not found"

    job.status = "MATCHED"  # send back to queue
    db.session.commit()

    return jsonify({"status": "retry_started"})


# ===============================
# APPLY NOW (MANUAL TRIGGER)
# ===============================
@app.route("/apply-now/<int:job_id>")
@login_required
def apply_now(job_id):

    job = JobApplication.query.get(job_id)

    if not job:
        return "Job not found"

    from apply.apply_router import apply_to_job

    result = apply_to_job(
        job.job_url,
        current_user.resume_path,
        job.cover_letter
    )

    job.status = result
    db.session.commit()

    return jsonify({"status": result})


# ===============================
# REAL-TIME STATUS CHECK
# ===============================
@app.route("/status")
def status():
    # future: track running state
    return jsonify({"running": False})


# ===============================
# UPLOAD RESUME
# ===============================
@app.route("/upload", methods=["POST"])
@login_required
def upload():

    file = request.files.get("resume")

    if not file:
        return redirect("/")

    os.makedirs("uploads", exist_ok=True)

    filename = secure_filename(file.filename)
    path = os.path.join("uploads", filename)

    file.save(path)

    current_user.resume_path = path
    db.session.commit()

    return redirect("/")


# ===============================
# LOGIN
# ===============================
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        user = User.query.filter_by(email=request.form["email"]).first()

        if user and check_password_hash(user.password_hash, request.form["password"]):
            login_user(user)
            return redirect("/")

        return "Invalid credentials"

    return render_template("login.html")


# ===============================
# REGISTER
# ===============================
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        existing = User.query.filter_by(email=request.form["email"]).first()

        if existing:
            return "User already exists"

        user = User(
            email=request.form["email"],
            password_hash=generate_password_hash(request.form["password"])
        )

        db.session.add(user)
        db.session.commit()

        return redirect("/login")

    return render_template("register.html")


# ===============================
# LOGOUT
# ===============================
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")


# ===============================
# START APP
# ===============================
if __name__ == "__main__":
    app.run(debug=True)