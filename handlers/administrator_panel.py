from flask import Blueprint, request, render_template, redirect, session
from utils.functions import *
from database import *
from config import *

administration_bp = Blueprint('administration', __name__, url_prefix='/administration')


@administration_bp.route("/", methods=["GET", "POST"])
def administration():
    if not session.get("is_administrator"):
        return render_template("error_page.html", error_code=403, error_message="Доступ запрещен"), 403

    psychologists = get_all(Psychologist)
    psychologists_result = []
    for psy in psychologists:
        psychologists_result.append({
            "id": psy.id,
            "name": psy.name,
            "email": psy.email,
            "login": psy.login,
            "password": psy.password
        })

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

    return render_template("administrator_panel.html", psychologists=psychologists_result, applications=app_result, meetings=meeting_result, reviews=review_result)

@administration_bp.route("/add_psychologist", methods=["POST"])
def add_psychologist():
    if not session.get("is_administrator"):
        return render_template("error_page.html", error_code=403, error_message="Доступ запрещен"), 403

    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    login = request.form.get("email").split("@")[0]

    create_psychologist(login, password, email, name)
    send_auth_data(email, password)
    return redirect("/administration")

@administration_bp.route("/edit_application", methods=["POST"])
def edit_application():
    if not session.get("is_administrator"):
        return render_template("error_page.html", error_code=403, error_message="Доступ запрещен"), 403

    app_id = request.args.get("app_id")
    fullname = request.form.get("fullname")
    comment = request.form.get("comment")

    update_object(Application, app_id, fullname=fullname, comment=comment)
    return redirect("/administration")

@administration_bp.route("/edit_meeting", methods=["POST"])
def edit_meeting():
    if not session.get("is_administrator"):
        return render_template("error_page.html", error_code=403, error_message="Доступ запрещен"), 403

    meet_id = request.args.get("meet_id")
    fullname = request.form.get("fullname")
    description = request.form.get("description")
    date = request.form.get("date")

    update_object(Meeting, meet_id, fullname=fullname, description=description, date=date)
    return redirect("/administration")

@administration_bp.route("/edit_review", methods=["POST"])
def edit_review():
    if not session.get("is_administrator"):
        return render_template("error_page.html", error_code=403, error_message="Доступ запрещен"), 403

    rev_id = request.args.get("rev_id")
    email = request.form.get("email")
    description = request.form.get("description")
    rating = request.form.get("rating")

    update_object(Review, rev_id, email=email, description=description, rating=rating)
    return redirect("/administration")

@administration_bp.route("/edit_psychologist", methods=["POST"])
def edit_psychologist():
    if not session.get("is_administrator"):
        return render_template("error_page.html", error_code=403, error_message="Доступ запрещен"), 403

    psy_id = request.args.get("psy_id")
    name = request.form.get("name")
    email = request.form.get("email")
    login = request.form.get("login")
    password = request.form.get("password")

    update_object(Psychologist, psy_id, name=name, email=email, login=login, password=password)
    return redirect("/administration")

@administration_bp.route("delete", methods=["GET","POST"])
def delete():
    if not session.get("is_administrator"):
        return render_template("error_page.html", error_code=403, error_message="Доступ запрещен"), 403

    app_id = request.args.get("app_id")
    meet_id = request.args.get("meet_id")
    rev_id = request.args.get("rev_id")
    psy_id = request.args.get("psy_id")

    if app_id:
        delete_object(Application, app_id)
    elif meet_id:
        delete_object(Meeting, meet_id)
    elif rev_id:
        delete_object(Review, rev_id)
    elif psy_id:
        try:
            delete_object(Psychologist, psy_id)
        except:
            return "Невозможно удалить психолога, так как он связан с встречами", 400
    
    return redirect("/administration")

