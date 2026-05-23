
from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

class Psychologist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    name = db.Column(db.String(120), nullable=False)
    verification_code = db.Column(db.String(50))  # новое поле

    meetings = db.relationship('Meeting', backref='psychologist', lazy=True)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    meeting_done = db.Column(db.Boolean, default=False)


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    fullname = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)


class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    fullname = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    phone_number = db.Column(db.String(20), nullable=False)
    date = db.Column(db.String(50))
    psychologist_id = db.Column(db.Integer, db.ForeignKey('psychologist.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    email = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)




def create_psychologist(login, password, email, name, verification_code=None):
    obj = Psychologist(
        login=login,
        password=password,
        email=email,
        name = name,
        verification_code=verification_code
    )
    db.session.add(obj)
    db.session.commit()
    return obj


def create_user(email, meeting_done=False):
    obj = User(email=email, meeting_done=meeting_done)
    db.session.add(obj)
    db.session.commit()
    return obj


def create_application(fullname, email, phone_number):
    obj = Application(fullname=fullname, email=email, phone_number=phone_number)
    db.session.add(obj)
    db.session.commit()
    return obj


def create_meeting(fullname, description, phone_number, email, date, psychologist_id):
    obj = Meeting(
        fullname=fullname,
        description=description,
        phone_number=phone_number,
        email=email,
        date=date,
        psychologist_id=psychologist_id
    )
    db.session.add(obj)
    db.session.commit()
    return obj


def create_review(rating, description, email):
    obj = Review(rating=rating, description=description, email=email)
    db.session.add(obj)
    db.session.commit()
    return obj



def get_psychologist_email_by_id(psychologist_id):
    psychologist = Psychologist.query.get(psychologist_id)
    
    if psychologist:
        return psychologist.email
    
    return None

def get_psychologist_id_by_login(login):
    psychologist = Psychologist.query.filter_by(login=login).first()
    
    if psychologist:
        return psychologist.id
    
    return None

def get_all(model):
    return model.query.all()


def get_by_id(model, obj_id):
    return model.query.get(obj_id)


def get_user_by_email(email):
    return User.query.filter_by(email=email).first()


def get_psychologist_by_login(login):
    return Psychologist.query.filter_by(login=login).first()

def get_verification_code_by_login(login):
    psychologist = Psychologist.query.filter_by(login=login).first()
    if psychologist:
        return psychologist.verification_code
    return None




def get_today_meetings(psychologist_id):
    today = date.today().strftime("%Y-%m-%d")

    query = Meeting.query.filter_by(date=today)

    if psychologist_id:
        query = query.filter_by(psychologist_id=psychologist_id)

    return query.all()

def get_meetings_by_psychologist(psychologist_id):
    return Meeting.query.filter_by(psychologist_id=psychologist_id).all()


def get_meetings_by_phone(phone_number):
    return Meeting.query.filter_by(phone_number=phone_number).all()


def get_meetings_by_fullname(fullname):
    return Meeting.query.filter(Meeting.fullname.ilike(f"%{fullname}%")).all()


def get_meetings_with_psychologist():
    return db.session.query(Meeting, Psychologist).join(Psychologist).all()


def get_meetings_with_psychologist_info(psychologist_id):
    return db.session.query(Meeting, Psychologist)\
        .join(Psychologist)\
        .filter(Psychologist.id == psychologist_id)\
        .all()


def get_users_with_meeting():
    return User.query.filter_by(meeting_done=True).all()


def get_users_without_meeting():
    return User.query.filter_by(meeting_done=False).all()




def get_applications_by_email(email):
    return Application.query.filter_by(email=email).all()


def get_applications_by_phone(phone_number):
    return Application.query.filter_by(phone_number=phone_number).all()




def get_reviews_with_min_rating(min_rating):
    return Review.query.filter(Review.rating >= min_rating).all()


def get_reviews_by_email(email):
    return Review.query.filter_by(email=email).all()




def update_psychologist_password(psychologist_id, new_password):
    psychologist = Psychologist.query.get(psychologist_id)
    if not psychologist:
        return None  # Психолог не найден

    psychologist.password = new_password
    db.session.commit()
    return psychologist

def update_object(model, obj_id, **kwargs):
    obj = model.query.get(obj_id)
    if not obj:
        return None

    for key, value in kwargs.items():
        setattr(obj, key, value)

    db.session.commit()
    return obj


def update_user_meeting_status(user_id, status: bool):
    user = User.query.get(user_id)
    if user:
        user.meeting_done = status
        db.session.commit()
    return user

def update_verification_code(psychologist_id, new_code):
    psychologist = Psychologist.query.get(psychologist_id)
    if not psychologist:
        return None

    psychologist.verification_code = new_code
    db.session.commit()
    return psychologist




def delete_object(model, obj_id):
    obj = model.query.get(obj_id)
    if obj:
        db.session.delete(obj)
        db.session.commit()
    return obj



