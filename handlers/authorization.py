from flask import Blueprint, request, render_template, redirect, session
from utils.functions import *
from database import *
from config import ADMIN_LOGIN, ADMIN_PASSWORD

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route("/", methods=["GET", "POST"])
def psychologist_auth_page():
    return render_template("authorization_page.html",display="none")

@auth_bp.route("login", methods=[ "POST"])
def psychologist_login():
    if request.method == "POST":
        try:
            if request.form.get("login") == ADMIN_LOGIN and request.form.get("password") == ADMIN_PASSWORD:
                session["is_administrator"] = True
                session["user_id"] = "admin"
                return redirect("/administration")
            

            if  get_psychologist_by_login(request.form.get("login")).password ==  request.form.get("password"):
                session["user_id"] = get_psychologist_by_login(request.form.get("login")).id
                session["is_psychologist"] = True
                return redirect("/dashboard")
            
            else:
                return render_template("authorization_page.html", message="Неверный логин или пароль", user_id=user_id, display="block")
        except:
            return render_template("authorization_page.html", message="Неверный логин или пароль",  display="block")

    



@auth_bp.route("forgot_password")
def forgot_password():
    user_id = request.args.get("user_id")
    code = generate_verification_code()
    update_verification_code(user_id, code)
    email = get_psychologist_email_by_id(user_id)
    send_auth_code(email, code)
    return render_template("code_confirmation.html")


@auth_bp.route("verify_code", methods=["POST"])
def verify_code():
    code_input = request.form.get("code")
    user_id = request.args.get("user_id") 

    if not user_id or not code_input:
        return "Неверные данные", 400

    psychologist = get_by_id(Psychologist, user_id)
    if not psychologist:
        return "Пользователь не найден", 404

    if psychologist.verification_code != code_input:
        return render_template("code_confirmation.html", message="Неверный код. Попробуйте снова.")

    new_password = generate_password()
    update_psychologist_password(user_id, new_password)
    update_object(Psychologist, user_id, password=new_password)

    send_new_password(psychologist.email, new_password)

    return render_template("authorization_page.html", message="Новый пароль отправлен на вашу почту!", display="none")
