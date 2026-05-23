from flask import Flask
from flask import Flask, request, render_template, redirect, session 
from utils.functions import *
from database import *
from handlers import dashboard, authorization, administrator_panel
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.register_blueprint(authorization.auth_bp)
app.register_blueprint(dashboard.dashboard_bp)
app.register_blueprint(administrator_panel.administration_bp)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "your_super_secret_key_here"
db.init_app(app)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("error_page.html", error_code=404, error_message="Страница не найдена"), 404

@app.route("/")
def hello_world():
    reviews = get_all(Review)[::-1]
    reviews_result = []
    for i in range(3):
        reviews_result.append({
            "description": reviews[i].description,
            "rating": reviews[i].rating
        })
    return render_template("main.html", reviews=reviews_result)
    

@app.route("/submit_review", methods=["POST"])
def submit_review():
    
    email = request.form.get("email")
    review = request.form.get("review")
    rating = request.form.get("rating")

    if get_user_by_email(email).meeting_done == True:
        create_review(rating, review, email)
    else:
        return "Вы не можете оставить отзыв, так как не посещали встречу", 403
    return "", 204


@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name")
    email = request.form.get("email")
    phone_number = request.form.get("phone_number")

    create_application(name, email, phone_number)
    create_user(email)

    send_mail_application(email, name)
    return "", 204

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        try:
            create_review("happy", "Профессионализм, искренность психолога, отзывчивость, внимательность к запросу, уютная и доброжелательная атмосфера на сессии. Появилась надежда, что со всеми проблемами я могу справиться.", "test1@vk.com")
            create_review("angry", "Пустая трата времени! Вместо помощи нагружали проблемами, задавали глупые вопросы и вообще никакого результата. Полностью разочарована!", "test2@vk.com")
            create_review("loving", "Очень благодарна психологу за поддержку и понимание. Благодаря его профессионализму и эмпатии, я смогла найти силы справиться с трудностями и начать новую главу в своей жизни.", "test3@vk.com")
            session.clear()
        except: pass
        print("База данных создана!")
        app.run(host="0.0.0.0", port=8000)
    
