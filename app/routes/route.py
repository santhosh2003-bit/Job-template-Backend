from flask import Blueprint, jsonify, request, flash
from werkzeug.utils import secure_filename
import os
from app.service.resume_processor import process_resume
from app.service.job_service import process_resume_and_find_jobs
from app.server import db
from flask_login import current_user
from app.db.jobsearchusagemodel import JobSearchUsage

api_routes = Blueprint("api", __name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

latest_uploaded_file = None


@api_routes.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Server is running ..."})


# @api_routes.route("/get_resume", methods=["POST"])
# def uplad_resume():

def allowed_file(filename):
    """Check if the file is a PDF."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@api_routes.route("/upload-resume", methods=["POST"])
def upload_resume():
    """Handle resume upload."""
    global latest_uploaded_file  # Use global to store the latest file

    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        # Store the latest uploaded file
        latest_uploaded_file = file_path

        return jsonify({"message": "File uploaded successfully"}), 200

    return jsonify({"error": "Invalid file type. Only PDFs are allowed"}), 400


@api_routes.route("/extract-info", methods=["POST"])
def extract_info():
    """Extract text from the latest uploaded PDF resume."""
    global latest_uploaded_file  # Get the last uploaded file

    if not latest_uploaded_file or not os.path.exists(latest_uploaded_file):
        return jsonify({"error": "No uploaded resume found"}), 400

    try:
        resume_data = process_resume(latest_uploaded_file)

        return jsonify(resume_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_routes.route("/find_job", methods=["POST"])
# def job_recommendations():
#     if "resume" not in request.files:
#         return jsonify({"error": "No file part"}), 400
#
#     resume_file = request.files["resume"]
#     job_profile = request.form.get("job_profile")
#
#     if resume_file.filename == "":
#         return jsonify({"error": "No selected file"}), 400
#
#     if not job_profile:
#         return jsonify({"error": "No Job profile found"}), 400
#
#
#     filename = secure_filename(resume_file.filename)
#     resume_path = os.path.join(UPLOAD_FOLDER, filename)
#     resume_file.save(resume_path)
#
#     try:
#         result_data = process_resume_and_find_jobs(resume_path, job_profile)
#
#         return jsonify(result_data), 200
#
#     finally:
#         if os.path.exists(resume_path):
#             os.remove(resume_path)
def job_recommendations():
    # Ensure the user is authenticated
    # if not current_user.is_authenticated:
    #     return jsonify({"error": "Authentication required"}), 401
    #
    # user_id = current_user.id
    #
    # # Retrieve the user's search usage record from the database
    # usage = JobSearchUsage.query.filter_by(user_id=user_id).first()
    # if usage and usage.search_count >= 5:
    #     return jsonify({"error": "Job search limit reached. You can search a maximum of 5 times."}), 403

    if "resume" not in request.files:
        return jsonify({"error": "No file part"}), 400

    resume_file = request.files["resume"]
    job_profile = request.form.get("job_profile")

    if resume_file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if not job_profile:
        return jsonify({"error": "No Job profile found"}), 400

    filename = secure_filename(resume_file.filename)
    resume_path = os.path.join(UPLOAD_FOLDER, filename)
    resume_file.save(resume_path)

    try:
        # Process the resume and find jobs
        result_data = process_resume_and_find_jobs(resume_path, job_profile)

        # Update or create the job search usage record
        # if usage:
        #     usage.search_count += 1
        #     usage.last_search = db.func.current_timestamp()
        # else:
        #     usage = JobSearchUsage(user_id=user_id, search_count=1)
        #     db.session.add(usage)
        # db.session.commit()

        return jsonify(result_data), 200

    finally:
        if os.path.exists(resume_path):
            os.remove(resume_path)