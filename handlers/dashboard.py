from flask import Blueprint, request, render_template, redirect, session
from utils.functions import *
from database import *
from config import *

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard_bp.route("/", methods=["GET", "POST"])
def dashboard():
    if not session.get("is_psychologist"):
        return render_template("error_page.html", error_code=403, error_message="Доступ запрещен"), 403
    psychologist_name = get_by_id(Psychologist, session.get("user_id")).name

    application = get_all(Application)
    app_result = []
    for app in application:
        app_result.append({
            "id": app.id,
            "fullname": app.fullname,
            "email": app.email,
            "phone_number": app.phone_number
        })

    meeting = get_meetings_by_psychologist(session.get("user_id"))
    meet_lenght = len(get_today_meetings(session.get("user_id")))
    meeting_result = []
    for meet in meeting:
        meeting_result.append({
            "id": meet.id,
            "fullname": meet.fullname,
            "description": meet.description,
            "date": meet.date,
            "phone_number": meet.phone_number
        })

    review = get_all(Review)
    review_result = []
    for rev in review:
        review_result.append({
            "id": rev.id,
            "email": rev.email,
            "description": rev.description,
            "rating": word_to_emoji[rev.rating]
        })


    return render_template("dashboard.html", applications=app_result, meetings=meeting_result, psychologist_name=psychologist_name , reviews=review_result, app_length=len(app_result), meet_length=meet_lenght, review_length=len(review_result))

@dashboard_bp.route("submit_application", methods=["POST"])
def submit_application():
    if not session.get("is_psychologist"):
        return render_template("error_page.html", error_code=403, error_message="Доступ запрещен"), 403
    application_id = request.args.get("application_id")
    application = get_by_id(Application, application_id)
    email = application.email
    description = request.form.get("description")
    date = request.form.get("date")
    psychologist_id = session.get("user_id")

    create_meeting(application.fullname, description, application.phone_number, email, date, psychologist_id)
    send_mail_planning(email, application.fullname, date)
    delete_object(Application, application_id)

    return redirect("/dashboard")

@dashboard_bp.route("submit_meeting", methods=["POST"])
def submit_meeting():
    if not session.get("is_psychologist"):
        return render_template("error_page.html", error_code=403, error_message="Доступ запрещен"), 403
    meeting_id = request.args.get("meeting_id")
    user_id = get_user_by_email(get_by_id(Meeting, meeting_id).email).id
    update_user_meeting_status(user_id, True)
    delete_object(Meeting, meeting_id)

    return redirect("/dashboard")