from flask import request, session
import mysql.connector
import re
import os
import uuid
from languages import translate

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


from icecream import ic
ic.configureOutput(prefix=f'----- | ', includeContext=True)


##############################
def db():
    db = mysql.connector.connect(
        host = "mysql",      # Replace with your MySQL server's address or docker service name "mysql"
        user = "root",  # Replace with your MySQL username
        password = "password",  # Replace with your MySQL password
        database = "new"   # Replace with your MySQL database name
    )
    cursor = db.cursor(dictionary=True)
    return db, cursor


##############################
def validate_user_logged():
    if not session.get("user"): raise Exception("new_ex user not logged")
    return session.get("user")


##############################
def send_email(user_name, user_last_name, user_email, user_verification_token, lan="dk"):
    try:
        # Create a gmail
        # Enable (turn on) 2 step verification/factor in the google account manager
        # Visit: https://myaccount.google.com/apppasswords

        # Email and password of the sender's Gmail account
        sender_email = "kamiweb1031@gmail.com"
        password = "bdqb aclo sysn hgrf"  # If 2FA is on, use an App Password instead

        # Receiver email address
        receiver_email = "kamiweb1031@gmail.com"
        
        # Create the email message
        message = MIMEMultipart()
        message["From"] = "Vejhylden"
        message["To"] = "kamiweb1031@gmail.com"
        message["Subject"] = translate("email_subject", lan)

        # Verification link
        verification_link = f"http://127.0.0.1/{lan}/verify/{user_verification_token}"

        # Body of the email
        body = f"""
        <h1>{ translate('thanks', lan) }, {user_name} {user_last_name} { translate('signing_up', lan) }</h1>
        <p>{ translate('verify_link', lan) }</p>
        <p><a href="{verification_link}">{ translate('click_here', lan) }</a></p>"""
        
        message.attach(MIMEText(body, "html"))

        # Connect to Gmail's SMTP server and send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Upgrade the connection to secure
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        ic("Email sent successfully!")

        return "email sent"

    except Exception as ex:
        ic(ex)
        raise Exception("cannot send email")
    finally:
        pass



##############################
def send_reset_email(user_email, reset_token, lan="dk"):
    from languages import translate

    sender_email = "kamiweb1031@gmail.com"
    password = "bdqb aclo sysn hgrf"
    receiver_email = "kamiweb1031@gmail.com"

    link = f"http://127.0.0.1/{lan}/reset-password/{reset_token}"

    subject = translate("reset_password", lan)
    body = f"""
        <h1>{translate("reset_email_greeting", lan)}</h1>
        <p>{translate("reset_email_instruction", lan)}</p>
        <p><a href="{link}">{translate("click_here", lan)}</a></p>
    """

    message = MIMEMultipart()
    message["From"] = "Vejhylden"
    message["To"] = "kamiweb1031@gmail.com"
    message["Subject"] = subject
    message.attach(MIMEText(body, "html"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

##############################
def send_deletion_email(user_name, user_last_name, user_email, lan="dk"):
    """
    Sender en bekræftelse til user_email om at kontoen er slettet.
    """
    try:
        sender_email = "kamiweb1031@gmail.com"
        password     = "bdqb aclo sysn hgrf"  # dit App Password

        # Sæt modtageren til den bruger, vi sletter
        receiver_email = "kamiweb1031@gmail.com"
        
        # Byg selve beskeden
        message = MIMEMultipart()
        message["From"]    = "Vejhylden <{}>".format(sender_email)
        message["To"]      = receiver_email
        message["Subject"] = translate("deletion_email_subject", lan)

        body = f"""
        <h1>{translate('deletion_email_greeting', lan)} {user_name} {user_last_name}</h1>
        <p>{translate('deletion_email_body', lan)}</p>
        """
        message.attach(MIMEText(body, "html"))

        # Send via Gmail SMTP
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())

        ic("Deletion email sent successfully!")
    except Exception as ex:
        ic("Error sending deletion email:", ex)
        # Du kan vælge at raise igen, eller bare logge
        raise



##############################
# def validate_user_password():
#     error = "web_ex password"
#     user_password = request.form.get("user_password", "")
#     if len(user_password) < 8:
#         raise Exception(error)
#     return user_password



##############################
USER_NAME_MIN = 2
USER_NAME_MAX = 20
USER_NAME_REGEX = f"^.{{{USER_NAME_MIN},{USER_NAME_MAX}}}$"
def validate_user_name():
    error = "new_ex user_name"
    user_name = request.form.get("user_name", "").strip()
    if not re.match(USER_NAME_REGEX, user_name): 
        raise Exception(error)
    return user_name



##############################
USER_LAST_NAME_MIN   = 2
USER_LAST_NAME_MAX   = 20
USER_LAST_NAME_REGEX = f"^.{{{USER_LAST_NAME_MIN},{USER_LAST_NAME_MAX}}}$"
def validate_user_last_name():
    error = "new_ex last name"
    user_last_name = request.form.get("user_last_name", "").strip()
    if not re.match(USER_LAST_NAME_REGEX, user_last_name):
        raise Exception(error)
    return user_last_name



##############################
USER_USERNAME_MIN   = 2
USER_USERNAME_MAX   = 20
USER_USERNAME_REGEX = f"^[A-Za-z0-9_]{{{USER_USERNAME_MIN},{USER_USERNAME_MAX}}}$"
def validate_user_username():
    error = "new_ex user_username"
    user_username = request.form.get("user_username", "").strip()
    if not re.match(USER_USERNAME_REGEX, user_username):
        raise Exception(error)
    return user_username



##############################
USER_PASSWORD_MIN   = 2
USER_PASSWORD_MAX   = 20
USER_PASSWORD_REGEX = f"^[A-Za-z0-9_]{{{USER_PASSWORD_MIN},{USER_PASSWORD_MAX}}}$"
def validate_user_password():
    error = "new_ex user_password"
    user_password = request.form.get("user_password", "")
    if not re.match(USER_PASSWORD_REGEX, user_password):
        raise Exception(error)
    return user_password



##############################
REGEX_PAGE_NUMBER = "^[1-9][0-9]*$"
def validate_page_number(page_number):
    error = "new_ex page number"
    page_number = page_number.strip()
    if not re.match(REGEX_PAGE_NUMBER, page_number): raise Exception(error)
    return int(page_number)



##############################
REGEX_EMAIL = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
def validate_user_email():
    error = f"new_ex email"
    user_email = request.form.get("user_email", "").strip()
    if not re.match(REGEX_EMAIL, user_email): raise Exception(error)
    return user_email



##############################
ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg", "gif"]
MAX_FILE_SIZE = 1 * 1024 * 1024  # 1MB - size in bytes
MAX_FILES = 3

def validate_item_images():
    images_names = []
    if "files" not in request.files:
        raise Exception("new_ex at least one file")
    
    files = [f for f in request.files.getlist('files') if f.filename]
    
    # TODO: Fix the validation for 0 files
    # if not files == [None]:
    #     raise Exception("web_ex at least one file")  

    if len(files) == 0:
        raise Exception("new_ex at least one file")
    if len(files) > MAX_FILES:
        raise Exception(f"new_ex max {MAX_FILES} files")

    for f in files:
        data = f.read()
        size = len(data)
        f.seek(0)

        name, ext = os.path.splitext(f.filename)
        ext = ext.lstrip(".").lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise Exception("new_ex file extension not allowed")
        if size > MAX_FILE_SIZE:
            raise Exception("new_ex file too large")

        new_name = f"{uuid.uuid4().hex}.{ext}"
        f.save(os.path.join("static/uploads", new_name))
        images_names.append(new_name)

    return images_names



    # for the_file in files:
    #     file_size = len(the_file.read())
    #     file_name, file_extension = os.path.splitext(the_file.filename)
    #     the_file.seek(0)
    #     file_extension = file_extension.lstrip(".")
    #     if file_extension not in ALLOWED_EXTENSIONS:
    #         raise Exception("new_ex file extension not allowed")  
    #     if file_size > MAX_FILE_SIZE:
    #         raise Exception("new_ex file too large")  
    #     new_file_name = f"{uuid.uuid4().hex}.{file_extension}"
    #     images_names.append(new_file_name)
    #     file_path = os.path.join("static/uploads", new_file_name)
    #     the_file.save(file_path)
        
    # return images_names


# OBS: HVAD BETYDER OVENSTÅENDE IFT STATIC/UPLOADS? DUMMY BILLEDER???


