import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
import ssl
import random
import string

sender = "danilrychcov@gmail.com"
password = "lrne juaf sety zyzc"


smtp_server = "smtp.gmail.com"
smtp_port = 587 



html_planning = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap" rel="stylesheet">
    <title>Встреча с психологом</title>
</head>
<body>
    <img src="https://github.com/danrcv0/RKSI_psychologists/blob/main/logo.png?raw=true" alt="logo">

    <h1>Здравствуйте, {{name}}!</h1>

    <p>Ваша встреча с психологом назначена на:</p>
    <h2 style="color:#ff7300; margin:10px 0;">{{date}}</h2>

    <p>
        Пожалуйста, зайдите вовремя и подготовьтесь к разговору.  
        Если возникнут вопросы — не стесняйтесь обращаться к нам.
    </p>

    <p>
        Если вам показалось, что психолог проявил непрофессионализм, вы можете оставить жалобу:
    </p>

    <a href="https://www.rksi.ru/contacts#" style="display:inline-block; text-decoration:none; color:#fff; background:#0000cc; padding:12px 20px; border-radius:8px; font-weight:700; margin-top:15px;">Оставить жалобу</a>

    <style>
        html {
            width: 100%;
            background-image: url("https://github.com/danrcv0/RKSI_psychologists/blob/main/mail_background.png?raw=true");
            background-size: cover;
        }
        body {
            width: 100%;
            padding: 20px;
            font-family: 'Inter', sans-serif;
        }
        img {
            width: 100px;
            margin-bottom: 15px;
        }
        h1 {
            font-size: 24px;
            font-weight: 900;
            margin: 0 0 10px 0;
        }
        h2 {
            font-size: 22px;
            font-weight: 800;
            margin: 0;
        }
        p {
            font-size: 16px;
            font-weight: 300;
            margin: 0 0 10px 0;
            line-height: 1.5;
        }
    </style>
</body>
</html>
"""

html_application = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap" rel="stylesheet">
    <title>Заявка получена</title>
</head>

<body>
    <img src="https://github.com/danrcv0/RKSI_psychologists/blob/main/logo.png?raw=true" alt="logo">

    <h1>Здравствуйте, {{name}}!</h1>

    <p>Ваша заявка была успешно отправлена и будет рассмотрена в ближайшее время.</p>

    <p>
        С вами обязательно свяжется психолог, чтобы назначить встречу в удобное для вас время.
    </p>

    <p>
        Если вам кажется, что ответы задерживаются, вы можете обратиться напрямую:
    </p>

    <p style="font-size:16px; font-weight:500; margin-top:10px;">
        📞 8 (863) 206-88-88 доб. 1021 — Бокулярова Ирина Николаевна<br>
        📞 8 (863) 206-88-88 доб. 1012 — Нефедова Евгения Михайловна
    </p>

    <style>
        html {
            width: 100%;
            background-image: url("https://github.com/danrcv0/RKSI_psychologists/blob/main/mail_background.png?raw=true");
            background-size: cover;
        }
        body {
            width: 100%;
            padding: 20px;
            font-family: 'Inter', sans-serif;
        }
        img {
            width: 100px;
            margin-bottom: 15px;
        }
        h1 {
            font-size: 24px;
            font-weight: 900;
            margin: 0 0 10px 0;
        }
        p {
            font-size: 16px;
            font-weight: 300;
            margin: 0 0 10px 0;
            line-height: 1.5;
        }
    </style>
</body>
</html>
"""
html_verification_code = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap" rel="stylesheet">

    <title>Код верификации</title>
</head>

<body>
    <img src="https://github.com/danrcv0/RKSI_psychologists/blob/main/logo.png?raw=true" alt="logo">

    <h1>Ваш код подтверждения</h1>

    <p>Пожалуйста, используйте следующий код для завершения верификации:</p>

    <h2 style="font-size: 28px; font-weight: 900; margin: 15px 0;"> {{code}} </h2>

    <p>
        <b>Важно!</b> Никому не сообщайте этот код.
    </p>

    <style>
        html {
            width: 100%;
            background-image: url("https://github.com/danrcv0/RKSI_psychologists/blob/main/mail_background.png?raw=true");
            background-size: cover;
        }

        body {
            width: 100%;
            padding: 20px;
            font-family: 'Inter', sans-serif;
        }

        img {
            width: 100px;
            height: 43px;
        }

        h1 {
            font-size: 24px;
            font-weight: 900;
            margin: 0 0 10px 0;
        }

        h2 {
            color: #ff7300;
        }

        p {
            margin: 0 0 10px 0;
            width: 280px;
            font-size: 16px;
            font-weight: 300;
        }

        b {
            font-weight: 700;
        }
    </style>
</body>
</html>
"""

html_new_password = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap" rel="stylesheet">

    <title>Новый пароль</title>
</head>

<body>
    <img src="https://github.com/danrcv0/RKSI_psychologists/blob/main/logo.png?raw=true" alt="logo">

    <h1>Ваш новый пароль</h1>

    <p>Пожалуйста, используйте следующий пароль для входа в систему:</p>

    <h2 style="font-size: 28px; font-weight: 900; margin: 15px 0;"> {{password}} </h2>

    <p>
        <b>Важно!</b> Никому не сообщайте этот пароль.
    </p>

    <style>
        html {
            width: 100%;
            background-image: url("https://github.com/danrcv0/RKSI_psychologists/blob/main/mail_background.png?raw=true");
            background-size: cover;
        }

        body {
            width: 100%;
            padding: 20px;
            font-family: 'Inter', sans-serif;
        }

        img {
            width: 100px;
            height: 43px;
        }

        h1 {
            font-size: 24px;
            font-weight: 900;
            margin: 0 0 10px 0;
        }

        h2 {
            color: #ff7300;
        }

        p {
            margin: 0 0 10px 0;
            width: 280px;
            font-size: 16px;
            font-weight: 300;
        }

        b {
            font-weight: 700;
        }
    </style>
</body>
</html>
"""

html_send_auth_data = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap" rel="stylesheet">

    <title>Данные для входа</title>
</head>

<body>
    <img src="https://github.com/danrcv0/RKSI_psychologists/blob/main/logo.png?raw=true" alt="logo">

    <h1>Добро пожаловать!</h1>

    <p>Для вас был создан аккаунт психолога.</p>

    <p><b>Ваши данные для входа:</b></p>

    <p>
        Логин: <b> {{email}} </b><br>
        Пароль: <b> {{password}} </b>
    </p>

    <p>
        Вы можете войти в систему и начать работу.
    </p>

    <style>
        html {
            width: 100%;
            background-image: url("https://github.com/danrcv0/RKSI_psychologists/blob/main/mail_background.png?raw=true");
            background-size: cover;
        }

        body {
            width: 100%;
            padding: 20px;
            font-family: 'Inter', sans-serif;
        }

        img {
            width: 100px;
            height: 43px;
        }

        h1 {
            font-size: 24px;
            font-weight: 900;
            margin: 0 0 15px 0;
        }

        p {
            margin: 0 0 10px 0;
            width: 280px;
            font-size: 16px;
            font-weight: 300;
        }

        b {
            font-weight: 700;
        }
    </style>
</body>
</html>
"""

def send_mail_application(to, name):
    # Создаем письмо
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Заявка принята"
    msg["From"] = formataddr(("Психологи РКСИ", sender))
    msg["To"] = to
    
    # Отправка
    html_content = html_application.replace("{{name}}", f"{name}")
    msg.attach(MIMEText(html_content, "html", "utf-8"))
    
    try:
        
        context = ssl.create_default_context()
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls(context=context)  # Активируем шифрование с контекстом
            server.login(sender, password)
            
            
            server.sendmail(sender, to, msg.as_string())
            server.quit()
            
        print("✅ Письмо успешно отправлено через Gmail!")
        return True
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def send_mail_planning(to, name, date):
    # Создаем письмо
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Запланирована встреча"
    msg["From"] = formataddr(("Психологи РКСИ", sender))
    msg["To"] = to
    
    # Отправка
    html_content = html_planning.replace("{{name}}", name).replace("{{date}}", date)
    msg.attach(MIMEText(html_content, "html", "utf-8"))
    
    try:
        # Создаем SSL контекст
        context = ssl.create_default_context()
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls(context=context)  # Активируем шифрование с контекстом
            server.login(sender, password)
            
            # Преобразуем сообщение в строку и отправляем
            server.sendmail(sender, to, msg.as_string())
            server.quit()
            
        print("✅ Письмо успешно отправлено через Gmail!")
        return True
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def send_auth_code(to, code):
    # Создаем письмо
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Код для авторизации"
    msg["From"] = formataddr(("Психологи РКСИ", sender))
    msg["To"] = to
    
    # Отправка
    html_content = html_verification_code.replace("{{code}}", code)
    msg.attach(MIMEText(html_content, "html", "utf-8"))
    
    try:
        # Создаем SSL контекст
        context = ssl.create_default_context()
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls(context=context)  # Активируем шифрование с контекстом
            server.login(sender, password)
            
            # Преобразуем сообщение в строку и отправляем
            server.sendmail(sender, to, msg.as_string())
            server.quit()
            
        print("✅ Письмо успешно отправлено через Gmail!")
        return True
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def send_new_password(to, pswrd):
    # Создаем письмо
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Новый пароль"
    msg["From"] = formataddr(("Психологи РКСИ", sender))
    msg["To"] = to
    
    # Отправка
    html_content = html_new_password.replace("{{password}}", pswrd)
    msg.attach(MIMEText(html_content, "html", "utf-8"))
    
    try:
        # Создаем SSL контекст
        context = ssl.create_default_context()
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls(context=context)  # Активируем шифрование с контекстом
            server.login(sender, password)
            
            # Преобразуем сообщение в строку и отправляем
            server.sendmail(sender, to, msg.as_string())
            server.quit()
            
        print("✅ Письмо успешно отправлено через Gmail!")
        return True
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False
    
def send_auth_data(email, pswrd):
    # Создаем письмо
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Новый пароль"
    msg["From"] = formataddr(("Психологи РКСИ", sender))
    msg["To"] = email
    
    # Отправка
    html_content = html_send_auth_data.replace("{{email}}", email.split("@")[0]).replace("{{password}}", pswrd)
    msg.attach(MIMEText(html_content, "html", "utf-8"))
    
    try:
        # Создаем SSL контекст
        context = ssl.create_default_context()
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls(context=context)  # Активируем шифрование с контекстом
            server.login(sender, password)
            
            # Преобразуем сообщение в строку и отправляем
            server.sendmail(sender, email, msg.as_string())
            server.quit()
            
        print("✅ Письмо успешно отправлено через Gmail!")
        return True
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False
    
def generate_verification_code():
    return ''.join(str(random.randint(0, 9)) for _ in range(6))

def generate_password(length=8):
    chars = string.ascii_letters + string.digits  # a-zA-Z0-9
    password = ''.join(random.choice(chars) for _ in range(length))
    return password
