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


# Validate user login status
##############################
def validate_user_logged():
    if not session.get("user"): raise Exception("new_ex user not logged")
    return session.get("user")


# Send verification email after user registration
##############################
def send_email(user_name, user_last_name, user_email, user_verification_token, lan="dk"):
    try:
        # Email and password of the sender's Gmail account
        sender_email = "kamiweb1031@gmail.com"
        password = "bdqb aclo sysn hgrf"  # If 2FA is on, use an App Password instead

        # Receiver email address
        receiver_email = "kamiweb1031@gmail.com"
        # With correct mail:
        # receiver_email = user_email

        
        # Create the email message
        message = MIMEMultipart()
        message["From"] = "Vejhylden"
        message["To"] = "kamiweb1031@gmail.com"
        message["Subject"] = translate("email_subject", lan)
        # With correct mail:
        # message["To"] = receiver_email

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


# Send password reset email
##############################
def send_reset_email(user_email, reset_token, lan="dk"):
    from languages import translate

    # Email and password of the sender's Gmail account
    sender_email = "kamiweb1031@gmail.com"
    password = "bdqb aclo sysn hgrf"
    receiver_email = "kamiweb1031@gmail.com"

    link = f"http://127.0.0.1/{lan}/reset-password/{reset_token}"

    # Create the email message
    subject = translate("reset_password", lan)
    body = f"""
        <h1>{translate("reset_email_greeting", lan)}</h1>
        <p>{translate("reset_email_instruction", lan)}</p>
        <p><a href="{link}">{translate("click_here", lan)}</a></p>
    """

    # Create a multipart message
    message = MIMEMultipart()
    message["From"] = "Vejhylden"
    message["To"] = "kamiweb1031@gmail.com"
    message["Subject"] = subject
    message.attach(MIMEText(body, "html"))

    # Connect to Gmail's SMTP server and send the email
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())


# Send deletion confirmation email after user account deletion
##############################
def send_deletion_email(user_name, user_last_name, user_email, lan="dk"):
    """
    Sender en bekræftelse til user_email om at kontoen er slettet.
    """
    try:
        sender_email = "kamiweb1031@gmail.com"
        password     = "bdqb aclo sysn hgrf"  # dit App Password

        # Set the receiver email to the user's email
        receiver_email = "kamiweb1031@gmail.com"
        
        # Build message
        message = MIMEMultipart()
        message["From"]    = "Vejhylden <{}>".format(sender_email)
        message["To"]      = receiver_email
        message["Subject"] = translate("deletion_email_subject", lan)

        # Body of the email
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
        # You can choose to raise again or just log
        raise


# Send block/unblock emails
##############################
def send_user_block_email(user_email: str, user_name: str, user_last_name: str, blocked: bool, lan="dk"):
    """
    Sender en mail til brugeren om at kontoen er (un)blokeret.
    """
    sender = "kamiweb1031@gmail.com"
    pwd    = "bdqb aclo sysn hgrf"

    # If blocked, send block email; if unblocked, send unblock email
    if blocked:
        subject = translate("email_subject_blocked", lan)
        body = f"""
            <h1>{translate('email_blocked_greeting', lan)} {user_name} {user_last_name}</h1>
            <p>{translate('email_blocked_body', lan)}</p>
        """
    else:
        subject = translate("email_subject_unblocked", lan)
        body = f"""
            <h1>{translate('email_unblocked_greeting', lan)} {user_name} {user_last_name}</h1>
            <p>{translate('email_unblocked_body', lan)}</p>
        """

    # Create the email message
    msg = MIMEMultipart()
    msg["From"]    = f"Vejhylden <{sender}>"
    msg["To"]      = "kamiweb1031@gmail.com"
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))

    # Send the email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as s:
            s.starttls()
            s.login(sender, pwd)
            s.send_message(msg)
        ic("Block/unblock mail sent")
    except Exception as e:
        ic("Error sending block mail:", e)


# Send item block/unblock emails
##############################
def send_item_block_email(user_email: str, user_name: str, user_last_name: str, item_name: str, blocked: bool, lan="dk"):
    """
    Sender en mail til ejeren af et item om at netop dét item er (un)blokeret.
    """
    sender = "kamiweb1031@gmail.com"
    pwd    = "bdqb aclo sysn hgrf"

    # If blocked, send block email; if unblocked, send unblock email
    if blocked:
        subject = translate("email_subject_item_blocked", lan)
        body = f"""
            <h1>{translate('email_item_blocked_greeting', lan)} {user_name} {user_last_name}</h1>
            <p>{translate('email_item_blocked_body', lan).format(item_name=item_name)}</p>
        """
    else:
        subject = translate("email_subject_item_unblocked", lan)
        body = f"""
            <h1>{translate('email_item_unblocked_greeting', lan)} {user_name} {user_last_name}</h1>
            <p>{translate('email_item_unblocked_body', lan).format(item_name=item_name)}</p>
        """

    # Create the email message
    msg = MIMEMultipart()
    msg["From"]    = f"Vejhylden <{sender}>"
    msg["To"]      = "kamiweb1031@gmail.com"
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))

    # Send the email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as s:
            s.starttls()
            s.login(sender, pwd)
            s.send_message(msg)
        ic("Item block/unblock mail sent")
    except Exception as e:
        ic("Error sending item-block mail:", e)


# Validate user input for name
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


# Validate user input for last name
##############################
USER_LAST_NAME_MIN   = 2
USER_LAST_NAME_MAX   = 20
USER_LAST_NAME_REGEX = f"^.{{{USER_LAST_NAME_MIN},{USER_LAST_NAME_MAX}}}$"
def validate_user_last_name():
    error = "new_ex last_name"
    user_last_name = request.form.get("user_last_name", "").strip()
    if not re.match(USER_LAST_NAME_REGEX, user_last_name):
        raise Exception(error)
    return user_last_name


# Validate user input for username
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


# Validate user input for password
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


# Validate user input for page number
##############################
REGEX_PAGE_NUMBER = "^[1-9][0-9]*$"
def validate_page_number(page_number):
    error = "new_ex page number"
    page_number = page_number.strip()
    if not re.match(REGEX_PAGE_NUMBER, page_number): raise Exception(error)
    return int(page_number)


# Validate user input for email
##############################
REGEX_EMAIL = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
def validate_user_email():
    error = f"new_ex email"
    user_email = request.form.get("user_email", "").strip()
    if not re.match(REGEX_EMAIL, user_email): raise Exception(error)
    return user_email


# Validate user input for images
##############################
ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg", "gif"]
MAX_FILE_SIZE = 5 * 1024 * 1024  # 1MB - size in bytes
MAX_FILES = 3

# Function to validate and save item images
def validate_item_images():
    images_names = []
    if "files" not in request.files:
        raise Exception("new_ex at least one file")
    
    # Get the list of files from the request
    files = [f for f in request.files.getlist('files') if f.filename]
    
# Check if there are no files or too many files
    if len(files) == 0:
        raise Exception("new_ex at least one file")
    if len(files) > MAX_FILES:
        raise Exception(f"new_ex max {MAX_FILES} files")

# Validate and save images
    for f in files:
        data = f.read()
        size = len(data)
        f.seek(0)

# Check file size and extension
        name, ext = os.path.splitext(f.filename)
        ext = ext.lstrip(".").lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise Exception("new_ex file extension not allowed")
        if size > MAX_FILE_SIZE:
            raise Exception("new_ex file too large")

# Generate a unique filename and save the file
        new_name = f"{uuid.uuid4().hex}.{ext}"
        f.save(os.path.join("static/uploads", new_name))
        images_names.append(new_name)

    return images_names
