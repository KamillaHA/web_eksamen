# Import required modules

from flask import Flask, render_template, session, request, redirect, url_for, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session
from decimal import Decimal
from datetime import datetime, date, timedelta
from collections import defaultdict
import x
import re
import time
import uuid
import os
import json
import languages
import requests
import traceback

app = Flask(__name__)

# Configure debug output with IceCream
from icecream import ic
ic.configureOutput(prefix=f'----- | ', includeContext=True)

# Configure Flask session
app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Set the secret key for session management
app.config['SECRET_KEY'] = os.environ.get(
    'SECRET_KEY',
    'h7G9kL!2pQzX4vNwR8s6HGa'  # din fallback
)

# Initialize the x module
##############################
@app.context_processor
def inject_user():
    # makes `user` available in every template
    return {"user": session.get("user")}


# Make helper functions available in all templates
##############################
@app.context_processor
def utility_processor():
    def image_path(filename):
        # If the filename is None or empty, return a placeholder image
        if not filename:
            return url_for("static", filename="images/placeholder.png")
        """Returner den korrekte static-sti til billedet."""

        # build absolute paths to upload and image dirs
        upload_fp = os.path.join(app.static_folder, "uploads", filename)
        image_fp  = os.path.join(app.static_folder, "images", filename)

        # choose existing folder or fallback
        if os.path.isfile(upload_fp):
            folder = "uploads"
        elif os.path.isfile(image_fp):
            folder = "images"
        else:
            folder = "uploads"   # fallback if none exists


        # Return the URL - use url_for to generate the URL for the static file
        return url_for("static", filename=f"{folder}/{filename}")
    return dict(image_path=image_path)


# Disable caching for all responses
##############################
@app.after_request
def disable_cache(response):
    """
    This function automatically disables caching for all responses.
    It is applied after every request to the server.
    """
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


# GET route for fetching exchange rates
##############################
@app.get("/rates")
def get_rates():
    try:
        # Fetch exchange rates from the external API
        data = requests.get("https://open.er-api.com/v6/latest/USD")
        ic(data.json())
        # Save the rates to a file for later use
        with open("rates.txt", "w") as file:
            file.write(data.text)
        return data.json()
    except Exception as ex:
        ic(ex)


# GET route for verifying user accounts
##############################
@app.get("/<lan>/verify/<token>")
def verify_account(token, lan="dk"):
    try:
        # Validate the token and update the user's verification status
        db, cursor = x.db()
        q = """UPDATE users SET user_verified_at = NOW()
            WHERE user_verification_token = %s AND user_verified_at IS NULL"""
        # Execute the query with the provided token - mark user as verified
        cursor.execute(q, (token,))
        if cursor.rowcount != 1:
            return languages.translate("already_verified", lan)
        db.commit()
        return languages.translate("verification_ok", lan)
    except Exception as ex:
        ic(ex)
        return languages.translate("verification_error", lan)
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


# GET route for the forgot password page
##############################
@app.get("/<lan>/forgot-password")
def forgot_password(lan="dk"):
    return render_template("_forgot_password.html", lan=lan, translate=languages.translate)


# POST route for handling forgot password requests
##############################
@app.post("/<lan>/forgot-password")
def post_forgot_password(lan="dk"):

    # Validate the user's email input
    user_email = request.form.get("user_email")
    db, cursor = x.db()
    cursor.execute("SELECT * FROM users WHERE user_email = %s", (user_email,))
    user = cursor.fetchone()

    # If the user does not exist, redirect with an error message
    if not user:
        session["toast_message"] = "email not found"
        session["toast_status"] = "error"
        return redirect(url_for("forgot_password", lan=lan))

    # If the user exists, generate a reset token and set its expiration
    reset_token = str(uuid.uuid4())
    expires = datetime.utcnow() + timedelta(hours=1)

    # Update the user's record with the reset token and expiration time
    cursor.execute("""
    UPDATE users
    SET user_password_reset_token = %s,
        user_password_reset_expires = %s
    WHERE user_email = %s
""", (reset_token, expires, user_email))
    db.commit()
    cursor.close(); db.close()

    # Send the reset email with the token
    x.send_reset_email(user_email, reset_token, lan)

    # Set a success message in the session and redirect to the login page
    session["toast_message"] = "A reset link has been sent"
    session["toast_status"] = "ok"
    return redirect(url_for("login", lan=lan))


# GET route for the reset password page
##############################
@app.get("/<lan>/reset-password/<token>")
def reset_password(token, lan="dk"):
    return render_template("_reset_password.html", token=token, lan=lan, translate=languages.translate)


# POST route for handling password reset requests
##############################
@app.post("/<lan>/reset-password/<token>")
def post_reset_password(token, lan="dk"):

    # Validate the token and new password
    new_pw = request.form.get("new_password", "").strip()
    # Check if the new password matches the required regex
    if not re.match(x.USER_PASSWORD_REGEX, new_pw):
        session["toast_message"] = "invalid password"
        session["toast_status"] = "error"
        return redirect(request.url)

    # Hash the new password
    hashed_pw = generate_password_hash(new_pw)
    db, cursor = x.db()
    cursor.execute("""
    SELECT * FROM users
    WHERE user_password_reset_token = %s
    AND user_password_reset_expires > NOW()
    """, (token,))
    user = cursor.fetchone()

    # If the user does not exist or the token is invalid, return an error
    if not user:
        return "invalid token"

    # Update the user's password and clear the reset token and expiration
    cursor.execute("""
    UPDATE users
    SET user_password = %s,
        user_password_reset_token = NULL,
        user_password_reset_expires = NULL,
        user_updated_at = NOW()
    WHERE user_pk = %s
    """, (hashed_pw, user["user_pk"]))
    db.commit()
    cursor.close(); db.close()

    # Set a success message in the session and redirect to the login page
    session["toast_message"] = "password success"
    session["toast_status"] = "ok"
    return redirect(url_for("login", lan=lan))


# GET route for the index page
##############################
@app.get("/")
@app.get("/<lan>/")
def index(lan="dk"):
    user = session.get("user")
    if lan not in languages.translations:
        lan = "dk"
    # If user is logged in, redirect to profile
    try:
        db, cursor = x.db()
        q = """
        SELECT items.*, images.*
        FROM items
        LEFT JOIN images
        ON items.item_pk = images.item_id
        AND images.image_deleted_at IS NULL
        JOIN users
        ON items.item_created_by = users.user_pk
        WHERE users.user_is_blocked = 0
        AND items.item_deleted_at IS NULL
        AND items.item_is_blocked = 0
        ORDER BY items.item_created_at DESC
        LIMIT 2
        """
        cursor.execute(q)
        items = cursor.fetchall()

# if the user is logged in, we can show the items
        for it in items:
            if isinstance(it.get("item_price"), Decimal):
                it["item_price"] = float(it["item_price"])

# get rates from the rates.txt file
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        rates_file = os.path.join(BASE_DIR, "rates.txt")

        rates = ""
        with open(rates_file, "r") as file:
            rates = file.read() # this is text that looks like json
        # Convert the text rates to json
        rates = json.loads(rates)

# Render the index template with the items and rates
        return render_template("index.html", title="Vejhylden", items=items, rates=rates, translate=languages.translate, lan=lan, x=x)
    except Exception:
        return "ups"
    finally:
        # Ensure the database connection is closed
            if cursor:
                cursor.close()
            if db:
                db.close()


# GET route for the signup page
##############################
@app.get("/signup")
@app.get("/<lan>/signup")
def signup(lan="dk"):
    try:
        return render_template("signup.html", title="Signup", x=x, translate=languages.translate, lan=lan)
    except Exception as ex:
        ic(ex)
        return "error loading signup page"
    finally:
        pass


# POST route for handling user signup
##############################
@app.post("/signup")
@app.post("/<lan>/signup")
def post_signup(lan="dk"):
    # Save the old values to repopulate the form in case of errors
    try:
        user_username = x.validate_user_username()
        user_name = x.validate_user_name()
        user_last_name = x.validate_user_last_name()
        user_email = x.validate_user_email()
        user_password = x.validate_user_password()
        hashed_password = generate_password_hash(user_password)
        user_verification_token = str(uuid.uuid4())

        # Check if the username already exists
        q = """INSERT INTO users
        (user_username, user_name, user_last_name, user_email,
        user_password, user_verification_token, user_verified_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s)"""

        # Insert the new user into the database
        db, cursor = x.db()
        cursor.execute(q, (user_username, user_name, user_last_name, user_email, hashed_password, user_verification_token, None))
        if cursor.rowcount != 1: raise Exception("System under maintenance")

        # Commit the changes to the database
        db.commit()

        # Send a verification email to the user
        try:
            ic("Sending email...")
            x.send_email(user_name, user_last_name, user_email, user_verification_token, lan=lan)
            ic("Done sending email.")
        except Exception as mail_ex:
            ic(f"Email-fejl: {mail_ex} (brugeren er oprettet)")

        # Toast message to show the user that the signup was successful
        session["toast_message"] = languages.translate("toast_signup_ok", lan)
        session["toast_status"] = "ok"
        session["toast_ttl"] = "4000"

        # Redirect to the login page
        return redirect(url_for("login", lan=lan))

    # Handle any exceptions that occur during the signup process
    except Exception as ex:
        ic(ex)
        traceback.print_exc()
        if "db" in locals(): db.rollback()
        # If an error occurs, we need to repopulate the form with the old values
        old_values = request.form.to_dict()
        if "username" in str(ex):
            old_values.pop("user_username", None)
            return render_template("signup.html",
                error_message="Invalid username", old_values=old_values, user_username_error="input_error", x=x, translate=languages.translate, lan=lan)
        if "first name" in str(ex):
            old_values.pop("user_name", None)
            return render_template("signup.html",
                error_message="Invalid name", old_values=old_values, user_name_error="input_error", x=x, translate=languages.translate, lan=lan)
        if "last name" in str(ex):
            old_values.pop("user_last_name", None)
            return render_template("signup.html",
                error_message="Invalid last name", old_values=old_values, user_last_name_error="input_error", x=x, translate=languages.translate, lan=lan)
        if "Invalid email" in str(ex):
            old_values.pop("user_email", None)
            return render_template("signup.html",
                error_message="Invalid email", old_values=old_values, user_email_error="input_error", x=x, translate=languages.translate, lan=lan)
        if "password" in str(ex):
            old_values.pop("user_password", None)
            return render_template("signup.html",
                error_message="Invalid password", old_values=old_values, user_password_error="input_error", x=x, translate=languages.translate, lan=lan)
        if "user_email" in str(ex):
            return redirect(url_for("signup",
                error_message="Email already exists", old_values=old_values, email_error=True, lan=lan))
        if "user_username" in str(ex):
            return redirect(url_for("signup",
                error_message="Username already exists", old_values=request.form, user_username_error=True, lan=lan))
        return redirect(url_for("signup", error_message=ex.args[0]))
    # Handle any cleanup or closing of resources
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


# GET route for the login page
##############################
@app.get("/login")
@app.get("/<lan>/login")
def login(lan="dk"):
    try:
        return render_template("login.html", title="Login", x=x, translate=languages.translate, lan=lan)
    except Exception as ex:
        ic(ex)
        return "error loading login page"
    finally:
        pass


# POST route for handling user login
##############################
@app.post("/login")
@app.post("/<lan>/login")
def post_login(lan="dk"):
    # Save the old values to repopulate the form in case of errors
    old = {}
    try:
        # Validate input fields
        user_email    = x.validate_user_email()
        user_password = x.validate_user_password()
        old["user_email"] = user_email

        # Get the user from the database
        db, cursor = x.db()
        cursor.execute("""
            SELECT user_pk, user_name, user_last_name,
                user_username, user_email, user_password,
                user_is_admin, user_verified_at, user_is_blocked
            FROM users
            WHERE user_email = %s AND user_deleted_at IS NULL
        """, (user_email,))
        user = cursor.fetchone()

        # Check if email exists
        if not user:
            raise Exception("User not found")

        # Check password
        if not check_password_hash(user["user_password"], user_password):
            raise Exception("Invalid password")

        # Check if the user is blocked
        if user.get("user_is_blocked"):
            session["toast_message"] = languages.translate("login_error_blocked", lan)
            session["toast_status"]  = "error"
            session["toast_ttl"]     = "4000"
            return redirect(url_for("login", lan=lan))

        # Check if the user is verified
        if not user.get("user_verified_at") and not user.get("user_is_admin"):
            session["toast_message"] = languages.translate("toast_login_error", lan)
            session["toast_status"]  = "error"
            session["toast_ttl"]     = "4000"
            return redirect(url_for("login", lan=lan))

        # Everything is fine, we can log the user in
        user.pop("user_password")
        session["user"] = user
        return redirect(url_for("admin" if user["user_is_admin"] else "profile", lan=lan))

    except Exception as ex:
        err = str(ex)
        # Show error messages based on the type of error
        email_err    = (err == "User not found")
        password_err = (err == "Invalid password")

        # Try to translate the error message based on the language
        if email_err:
            msg = languages.translate("login_error_no_user", lan)
        elif password_err:
            msg = languages.translate("login_error_wrong_password", lan)
        else:
            msg = languages.translate("login_error_generic", lan)

        # Close the cursor and database connection
        try:
            cursor.close()
            db.close()
        except:
            pass

        # Re-render login template with old values and error messages
        return render_template(
            "login.html",
            x=x,
            translate=languages.translate,
            lan=lan,
            old_values=old,
            user_email_error=email_err,
            user_password_error=password_err
            )

    finally:
        # Ensure the database connection is closed
        if "cursor" in locals(): cursor.close()
        if "db"     in locals(): db.close()


# GET route for the admin dashboard
##############################
@app.get("/admin")
@app.get("/<lan>/admin")
def admin(lan="dk"):
    # Only admins can access this route
    user = session.get("user")
    if not user or not user.get("user_is_admin"):
        return abort(403)

    # Toggle item or user blocking
    try:
        db, cursor = x.db()
        toggle_item = request.args.get("toggle_item")
        updated_item = None

        # If toggle_item is provided, toggle the item's blocked status
        if toggle_item:
            cursor.execute("UPDATE items SET item_is_blocked = NOT item_is_blocked WHERE item_pk = %s", (toggle_item,))
            db.commit()

            # Fetch the updated item details
            cursor.execute("""
                SELECT *
                FROM items
                LEFT JOIN images ON items.item_pk = images.item_id AND images.image_deleted_at IS NULL
                WHERE items.item_pk = %s
            """, (toggle_item,))
            updated_item = cursor.fetchone()

            # Render the rates from the rates.txt file
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            rates_file = os.path.join(BASE_DIR, "rates.txt")
            with open(rates_file, "r") as file:
                rates = json.loads(file.read())

            # If the item was successfully updated, send a notification email
            if updated_item:
                cursor.execute("""
                    SELECT user_email, user_name, user_last_name
                    FROM users
                    WHERE user_pk = %s
                """, (updated_item["item_created_by"],))
                owner = cursor.fetchone()

                # Send email notification
                try:
                    x.send_item_block_email(
                        owner["user_email"],
                        owner["user_name"],
                        owner["user_last_name"],
                        updated_item["item_name"],
                        updated_item["item_is_blocked"],
                        lan=lan
                    )
                except Exception as mail_ex:
                    x.ic(f"Fejl ved afsendelse af item-blok mail: {mail_ex}")

                cursor.close()
                db.close()

                # Render the updated item fragment
                fragment = render_template(
                    "_admin_item.html",
                    item=updated_item,
                    rates=rates,
                    lan=lan,
                    translate=languages.translate,
                    x=x
                )
                # Return the fragment wrapped in a mixhtml tag for replacement
                return f"""
                <mixhtml mix-replace="#admin_item">
                {fragment}
                </mixhtml>
                """

        # If toggle_user is provided, toggle the user's blocked status
        toggle_user = request.args.get("toggle_user")
        if toggle_user:
            cursor.execute("UPDATE users SET user_is_blocked = NOT user_is_blocked WHERE user_pk = %s", (toggle_user,))
            db.commit()

            # Fetch the user details to send a notification email
            cursor.execute("""
                SELECT user_email, user_name, user_last_name, user_is_blocked
                FROM users
                WHERE user_pk = %s
            """, (toggle_user,))
            u = cursor.fetchone()

            cursor.execute("UPDATE items SET item_is_blocked = %s WHERE item_created_by = %s", (1 if u["user_is_blocked"] else 0, toggle_user))
            db.commit()

            # Send email notification to the user about their blocked status
            try:
                x.send_user_block_email(
                    u["user_email"], u["user_name"], u["user_last_name"], u["user_is_blocked"], lan=lan
                )
            except Exception as mail_ex:
                x.ic(f"Fejl ved afsendelse af blok-mail: {mail_ex}")

            # Fetch the updated user details to render the admin user fragment
            cursor.execute("SELECT * FROM users WHERE user_pk = %s", (toggle_user,))
            updated_user = cursor.fetchone()
            cursor.close()
            db.close()

            fragment = render_template(
                "_admin_user.html",
                user=updated_user,
                lan=lan,
                translate=languages.translate
            )
            # Return the fragment wrapped in a mixhtml tag for replacement
            return f"""
            <mixhtml mix-replace="#user">
            {fragment}
            </mixhtml>
            """

        # If no toggle_item or toggle_user, fetch all items and users
        single_item = None
        if toggle_item:
            cursor.execute("""
                SELECT *
                FROM items
                LEFT JOIN images ON items.item_pk = images.item_id AND images.image_deleted_at IS NULL
                WHERE items.item_pk = %s
            """, (toggle_item,))
            single_item = cursor.fetchone()

        # Fetch all items and users
        cursor.execute("""
            SELECT items.*, images.*
            FROM items
            LEFT JOIN images ON items.item_pk = images.item_id AND images.image_deleted_at IS NULL
            LEFT JOIN users ON items.item_created_by = users.user_pk
            WHERE users.user_is_blocked = 0 AND items.item_deleted_at IS NULL
            ORDER BY items.item_created_at DESC
        """)
        items = cursor.fetchall()
        items.sort(key=lambda i: i["item_name"].lower())

        # Group items by the first letter of their name
        grouped_items = defaultdict(list)
        for item in items:
            grouped_items[item["item_name"][0].upper()].append(item)

        cursor.execute("""
            SELECT *
            FROM users
            WHERE user_deleted_at IS NULL
            ORDER BY user_created_at DESC
        """)
        users = cursor.fetchall()
        admin_pk = session["user"]["user_pk"]
        users = [u for u in users if u["user_pk"] != admin_pk]

        # Convert Decimal prices to float for JSON serialization
        for it in items:
            if isinstance(it.get("item_price"), Decimal):
                it["item_price"] = float(it["item_price"])

        # Read the rates from the rates.txt file
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        rates_file = os.path.join(BASE_DIR, "rates.txt")
        with open(rates_file, "r") as f:
            rates = json.loads(f.read())

        # Sort users by username and group them by the first letter
        users.sort(key=lambda u: u["user_name"].lower())
        grouped_users = defaultdict(list)
        for user in users:
            grouped_users[user["user_name"][0].upper()].append(user)

        cursor.close()
        db.close()

        # Render the admin template with all the data
        return render_template(
            "admin.html",
            title="Admin",
            items=items,
            single_item=single_item,
            rates=rates,
            users=users,
            x=x,
            grouped_users=grouped_users,
            translate=languages.translate,
            lan=lan
        )

    # Handle any exceptions that occur during the admin process
    except Exception as ex:
        ic(ex)
        import traceback
        traceback.print_exc()
        return f"""
        <h1>Fejl i admin</h1>
        <pre>{traceback.format_exc()}</pre>
        """
    finally:
        pass


# GET route for the user profile page
##############################
@app.get("/profile")
@app.get("/<lan>/profile")
def profile(lan="dk"):
    # Get the user's session data
    user = session.get("user")
    # if user not logged in, redirect to login
    if not user:
        return redirect(url_for("login", lan=lan))
    # if admin, redirect to admin dashboard
    if user.get("user_is_admin"):
        return redirect(url_for("admin", lan=lan))
    # Validate the user session
    user_pk = user["user_pk"]

# Get the rates from the rates.txt file
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    rates_file = os.path.join(BASE_DIR, "rates.txt")
    with open(rates_file, "r") as f:
        rates = json.loads(f.read())

    # Fetch the user's items from the database
    db, cursor = x.db()
    cursor.execute("""
    SELECT *
    FROM items
    LEFT JOIN images
    ON items.item_pk = images.item_id
    AND images.image_deleted_at IS NULL
    WHERE items.item_created_by = %s
    AND items.item_deleted_at IS NULL
    AND items.item_is_blocked = 0
    ORDER BY items.item_created_at DESC
""", (user_pk,))
    user_items = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template("profile.html", title="Profile", x=x, items=user_items, rates=rates, translate=languages.translate, lan=lan)


# GET route for logging out
##############################
@app.get("/logout")
@app.get("/<lan>/logout")
def logout(lan="dk"):
    if "user" in session:
        session.pop("user")
    return redirect(url_for("login", lan=lan))


# GET route for fetching an item by its primary key (item_pk)
##############################
@app.get("/items/<item_pk>")
@app.get("/<lan>/items/<item_pk>")
def get_item_by_pk(item_pk, lan="dk"):
    lan = request.args.get('lan', 'dk')
    if lan not in ("dk","en"):
        lan = "dk"

    # Rates are loaded from a file
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    rates_file = os.path.join(BASE_DIR, "rates.txt")
    with open(rates_file, "r") as file:
        rates = json.loads(file.read())
        # Get item by primary key (item_pk)
    try:
        db, cursor = x.db()
        q = """
        SELECT *
        FROM items
        LEFT JOIN images
        ON items.item_pk = images.item_id
        AND images.image_deleted_at IS NULL
        WHERE items.item_pk = %s
    """

        # Execute the query with the provided item_pk
        cursor.execute(q, (item_pk,))
        item = cursor.fetchone()

        # If item has decimal price, convert it to float
        if item and isinstance(item.get("item_price"), Decimal):
            item["item_price"] = float(item["item_price"])

        html_item = render_template("_item.html", item=item, rates=rates, lan=lan,
            translate=languages.translate)
        return f"""
            <mixhtml mix-replace="#item">
                {html_item}
            </mixhtml>
        """
    # Handle exceptions that may occur during the database operations
    except Exception as ex:
        ic(ex)
        if "new_ex page number" in str(ex):
            return """
                <mixhtml mix-top="body">
                    page number invalid
                </mixhtml>
            """
        # worst case, we cannot control exceptions
        return """
            <mixhtml mix-top="body">
                ups
            </mixhtml>
        """
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


# GET route for fetching a single item fragment
##############################
@app.get("/items/fragment/<item_pk>")
@app.get("/<lan>/items/fragment/<item_pk>")
def get_item_fragment(item_pk, lan="dk"):
    # Database connection and cursor
    db, cursor = x.db()
    cursor.execute("""
        SELECT *
        FROM items
        LEFT JOIN images
        ON items.item_pk = images.item_id
        AND images.image_deleted_at IS NULL
        WHERE items.item_pk = %s
    """, (item_pk,))
    # Fetch the item from the database
    item = cursor.fetchone()
    cursor.close()
    db.close()

    # This is the fragment that will be replaced in the DOM without a full page reload
    fragment = render_template(
        "_user_single_item.html",
        item=item,
        lan=lan,
        translate=languages.translate,
        x=x
    )

    # Return the fragment wrapped in a mixhtml tag for replacement
    return f"""
<mixhtml mix-replace="#single_item_user">
    <section id="single_item_user">
    {fragment}
    </section>
    </mixhtml>
"""


# GET route for fetching an admin item fragment
##############################
@app.get("/admin/items/fragment/<int:item_pk>")
@app.get("/<lan>/admin/items/fragment/<int:item_pk>")
def get_admin_item_fragment(item_pk, lan="dk"):
    # Only admins can access this route
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    rates_file = os.path.join(BASE_DIR, "rates.txt")
    with open(rates_file, "r") as file:
        rates = file.read()
    rates = json.loads(rates)
    user = session.get("user")
    if not user or not user.get("user_is_admin"):
        return abort(403)

    # Validate the session
    db, cursor = x.db()
    cursor.execute("""
        SELECT *
        FROM items
        LEFT JOIN images
        ON items.item_pk = images.item_id
        AND images.image_deleted_at IS NULL
        WHERE items.item_pk = %s
    """, (item_pk,))
    item = cursor.fetchone()
    cursor.close(); db.close()

    # Render the admin item fragment
    html = render_template(
        "_admin_item.html",
        item=item,
        rates=rates,
        lan=lan,
        translate=languages.translate,
        x=x
    )

    # Wrap the HTML in a mixhtml tag for replacement
    return f"""
<mixhtml mix-replace="#single_item_admin">
    <section id="single_item_admin">
    {html}
    </section>
    </mixhtml>
"""


# GET route for fetching items by page number
##############################
@app.get("/items/page/<page_number>")
@app.get("/<lan>/items/page/<page_number>")
def get_items_by_page(page_number, lan="dk"):
    lan = request.args.get('lan', 'dk')
    if lan not in ("dk","en"):
        lan = "dk"
    # Validate the page number
    try:
        page_number = x.validate_page_number(page_number)
        items_per_page = 2
        offset = (page_number-1) * items_per_page
        extra_item = items_per_page + 1
        db, cursor = x.db()
        # Fetch items from the database with pagination
        q = """
        SELECT *
        FROM items
        LEFT JOIN images
        ON items.item_pk = images.item_id
        AND images.image_deleted_at IS NULL
        WHERE items.item_deleted_at IS NULL
        ORDER BY items.item_created_at DESC
        LIMIT %s OFFSET %s
        """
        cursor.execute(q, (extra_item, offset))
        items = cursor.fetchall()

        # Convert Decimal and DateTime fields to JSON serializable formats
        for it in items:
            for k, v in list(it.items()):
                if isinstance(v, Decimal):
                    it[k] = float(v)
                elif isinstance(v, (datetime, date)):
                    it[k] = v.isoformat()

        # If no items are found, return an empty response
        html = ""

        # Rates are loaded from a file
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        rates_file = os.path.join(BASE_DIR, "rates.txt")
        with open(rates_file, "r") as file:
            rates = file.read()
        rates = json.loads(rates)

        # Render the items as HTML cards
        for item in items[:items_per_page]:
            i = render_template("_card.html", item=item, rates=rates, lan=lan, translate=languages.translate)
            html += i
        button = render_template("_btn_more_items.html", page_number=page_number + 1, lan=lan, translate=languages.translate)
        # If there are fewer items than the extra_item, do not show the button
        if len(items) < extra_item: button = ""
        return f"""
            <mixhtml mix-bottom="#items">
                {html}
            </mixhtml>
            <mixhtml mix-replace="#btn_more_items">
                {button}
            </mixhtml>
            <mixhtml mix-function="add_markers_to_map">
                {json.dumps(items[:items_per_page])}
            </mixhtml>
        """
    # Handle exceptions that may occur during the database operations
    except Exception as ex:
        ic(ex)
        if "new_ex page number" in str(ex):
            return """
                <mixhtml mix-top="body">
                    page number invalid
                </mixhtml>
            """
        # worst case, we cannot control exceptions
        return """
            <mixhtml mix-top="body">
                ups
            </mixhtml>
        """
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


# POST route for creating a new item
##############################
@app.post("/item")
@app.post("/<lan>/item")
def create_item(lan="dk"):
    # Check if the user is logged in
    user = x.validate_user_logged()

    # Validate and get the form fields
    item_name    = request.form["item_name"].strip()
    item_address = request.form["item_address"].strip()
    item_price   = float(request.form["item_price"].strip().replace(",", "."))

    # Import requests for geocoding
    try:
        resp = requests.get(
            "https://nominatim.openstreetmap.org/search",
    params={
        "q": item_address,      # Adress as search query
        "format": "json",
        "countrycodes": "dk",   # Limit to Denmark
        "limit": 1,             # Only one result
        "addressdetails": 1     # (optional) also return details about the address
    },
    headers={"User-Agent": "my-flask-app/1.0"}
        )
        data = resp.json()
        latitude  = float(data[0]["lat"]) if data else 0.0
        longitude = float(data[0]["lon"]) if data else 0.0
    except:
        latitude = longitude = 0.0

    # Validate and save item images
    image_filenames = x.validate_item_images()
    img1, img2, img3 = (image_filenames + [None, None, None])[:3]

    # Open DB connection and cursor and insert the item
    db, cursor = x.db()
    cursor.execute(
        """
        INSERT INTO items
            (item_name,item_address,item_price,item_latitude,item_longitude,item_created_by)
        VALUES (%s,%s,%s,%s,%s,%s)
        """,
        (item_name, item_address, item_price,
            latitude, longitude, user["user_pk"])
    )
    item_pk = cursor.lastrowid

    # If there are no images, we insert NULLs
    cursor.execute(
        """
        INSERT INTO images
        (item_id, item_image, item_image_2, item_image_3)
        VALUES (%s,%s,%s,%s)
        """,
        (item_pk, img1, img2, img3)
    )

    db.commit()
    cursor.close()
    db.close()

    return redirect(url_for("profile", lan=lan))


# POST route for updating an existing item
##############################
@app.post("/items/<item_pk>")
@app.post("/<lan>/items/<item_pk>")
def update_item(item_pk, lan="dk"):
    # Check if the user is logged in
    user = x.validate_user_logged()

    # Validate the item
    item_name    = request.form["item_name"].strip()
    item_address = request.form["item_address"].strip()
    item_price   = request.form["item_price"].strip()

    # Open a database connection and cursor
    db, cursor = x.db()

    # Get the existing images for the item
    cursor.execute(
        "SELECT item_image, item_image_2, item_image_3 FROM images WHERE item_id = %s",
        (item_pk,)
    )
    # Fetch the existing images or set to empty dict if not found
    old = cursor.fetchone() or {}
    img1 = old.get("item_image")
    img2 = old.get("item_image_2")
    img3 = old.get("item_image_3")

    # This function checks the file extension and size, saves it, and returns the new filename
    def save_one(f):
        name, ext = os.path.splitext(f.filename)
        ext = ext.lstrip(".").lower()
        if ext not in x.ALLOWED_EXTENSIONS:
            raise Exception("new_ex file extension not allowed")
        data = f.read()
        size = len(data)
        f.seek(0)
        if size > x.MAX_FILE_SIZE:
            raise Exception("new_ex file too large")
        new_name = f"{uuid.uuid4().hex}.{ext}"
        f.save(os.path.join("static", "uploads", new_name))
        return new_name

    # For each file slot, check if the user has uploaded a file
    for slot_attr, var_name in [("file1", "img1"), ("file2", "img2"), ("file3", "img3")]:
        f = request.files.get(slot_attr)
        if f and f.filename:
            new_fn = save_one(f)
            if var_name == "img1":
                img1 = new_fn
            elif var_name == "img2":
                img2 = new_fn
            elif var_name == "img3":
                img3 = new_fn

    # This updates the item details in the database
    cursor.execute(
        """
        UPDATE items
        SET
        item_name       = %s,
        item_address    = %s,
        item_price      = %s,
        item_updated_at = NOW()
        WHERE item_pk = %s
        AND item_created_by = %s
        """,
        (item_name, item_address, item_price, item_pk, user["user_pk"])
    )

    # This updates the images for the item
    cursor.execute(
        """
        UPDATE images
        SET
        item_image   = %s,
        item_image_2 = %s,
        item_image_3 = %s
        WHERE item_id = %s
        """,
        (img1, img2, img3, item_pk)
    )

    # Commit changes to the database
    db.commit()

    # Fetch the updated item with its images
    cursor.execute("""
        SELECT *
        FROM items
        LEFT JOIN images
        ON items.item_pk = images.item_id
        AND images.image_deleted_at IS NULL
        WHERE items.item_pk = %s
    """, (item_pk,))
    updated = cursor.fetchone()

    # Close the cursor and database connection
    cursor.close()
    db.close()

    # Render the updated item as a single item fragment
    snippet = render_template(
        "_user_single_item.html",
        item=updated,
        lan=lan,
        translate=languages.translate,
        x=x
    )
    # If the request is an AJAX request, return the snippet wrapped in a mixhtml tag
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return f"""
<mixhtml mix-replace="#single_item_user">
    <section id="single_item_user">
    {snippet}
    </section>
    </mixhtml>
"""
    # If not an AJAX request, redirect to the profile page
    else:
        return redirect(url_for("profile", lan=lan))


# GET route for fetching a user by primary key (user_pk)
##############################
@app.get("/users/<user_pk>")
@app.get("/<lan>/users/<user_pk>")
def get_user_by_pk(user_pk, lan="dk"):
    lan = request.args.get('lan', 'dk')
    if lan not in ("dk","en"):
        lan = "dk"
    try:
        db, cursor = x.db()
        # Fetch the user from the database by primary key
        q = "SELECT * FROM users WHERE user_pk = %s"

        # Execute the query with the provided user_pk
        cursor.execute(q, (user_pk,))
        user = cursor.fetchone()

        # Get the rates from the rates.txt file
        rates= ""
        with open("rates.txt", "r") as file:
            rates = file.read() # this is text that looks like json
            rates = json.loads(rates)

        # Render the user as an HTML fragment
        html_user = render_template("_admin_user.html", user=user, lan=lan,
            translate=languages.translate)
        return f"""
            <mixhtml mix-replace="#user">
                {html_user}
            </mixhtml>
        """
    # Handle exceptions that may occur during the database operations
    except Exception as ex:
        ic(ex)
        if "new_ex page number" in str(ex):
            return """
                <mixhtml mix-top="body">
                    page number invalid
                </mixhtml>
            """
        # worst case, we cannot control exceptions
        return """
            <mixhtml mix-top="body">
                ups
            </mixhtml>
        """
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


# POST route for updating user profile
##############################
@app.post("/user")
@app.post("/<lan>/user")
def update_user(lan="dk"):

    # Her kan du tilføje validering á la x.validate_…
    # user = x.validate_user_logged()

    # Hent data fra formularen - skal der strip() på???????
    user_name       = request.form["user_name"]
    user_last_name  = request.form["user_last_name"]
    user_username   = request.form["user_username"]
    user_email      = request.form["user_email"]
    user_pk         = session["user"]["user_pk"]

    # Update the user in the database
    db, cursor = x.db()
    q = """
        UPDATE users
        SET
        user_name      = %s,
        user_last_name = %s,
        user_username  = %s,
        user_email     = %s,
        user_updated_at= NOW()
        WHERE user_pk = %s AND user_is_blocked = 0
    """
    # Execute the query with the provided user data
    cursor.execute(q, (user_name, user_last_name, user_username, user_email, user_pk))
    db.commit()
    cursor.close(); db.close()

    # Update the session with the new user data
    session["user"].update({
        "user_name":      user_name,
        "user_last_name": user_last_name,
        "user_username":  user_username,
        "user_email":     user_email
    })

    # Return redirect to the profile page
    profile = url_for("profile", lan=lan)
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        # MixHTML will see this and perform a client-side redirect
        return f'<div mix-redirect="{profile}"></div>'
    return redirect(profile)


# POST route for changing user password
##############################
@app.post("/user/password")
@app.post("/<lan>/user/password")
def change_password(lan="dk"):
    # Get the current user from the session
    current = request.form["current_password"]
    new_pw  = request.form["new_password"]
    confirm = request.form["new_password_confirm"]
    user_pk = session["user"]["user_pk"]

    # Check the current password against the stored hash
    db, cursor = x.db()
    cursor.execute("SELECT user_password FROM users WHERE user_pk = %s", (user_pk,))
    row = cursor.fetchone()
    if not row or not check_password_hash(row["user_password"], current):
        abort(400, "Wrong current password")
    if new_pw != confirm:
        abort(400, "New password doesn´t match confirmation")

    # Hash the new password and update it in the database
    hashed = generate_password_hash(new_pw)
    cursor.execute(
        "UPDATE users SET user_password = %s, user_updated_at = NOW() WHERE user_pk = %s",
        (hashed, user_pk)
    )
    db.commit()
    cursor.close(); db.close()

    return redirect(url_for("profile", lan=lan))


# POST route for soft-deleting a user profile
##############################
@app.delete("/user")
@app.delete("/<lan>/user")
def delete_user(lan="dk"):
    # Check if the user is logged in
    user_pk = session["user"]["user_pk"]
    db, cursor = x.db()
    # Make the query to soft-delete the user
    q = """
    UPDATE users
    SET
    user_deleted_at = NOW(),
    user_is_blocked  = 1
    WHERE user_pk = %s
    """
    # Execute the query to soft-delete the user
    cursor.execute(q, (user_pk,))
    db.commit()
    cursor.close()
    db.close()

    # Log out the user by clearing the session
    session.clear()

    # This will be handled by MixHTML to redirect the user to the login page
    return f'<div mix-redirect="{url_for("login", lan=lan)}"></div>'


# POST route for deleting a user profile
##############################
@app.post("/user/delete")
@app.post("/<lan>/user/delete")
def post_delete_user(lan="dk"):
    # Check if the user is logged in
    user = x.validate_user_logged()
    user_pk = user["user_pk"]

    # Get the current password from the form
    entered = request.form.get("current_password", "").strip()

    # Get the user details / hash from the database
    db, cursor = x.db()
    cursor.execute(
        "SELECT user_password, user_email, user_name, user_last_name "
        "FROM users WHERE user_pk = %s",
        (user_pk,)
    )
    row = cursor.fetchone()

    # If the row is empty or the password does not match, return an error
    if not row or not check_password_hash(row["user_password"], entered):
        cursor.close(); db.close()

        # Regenerate items and rates as in GET /profile …
        with open("rates.txt", "r") as f:
            rates = json.loads(f.read())
        db2, cursor2 = x.db()
        cursor2.execute("""
            SELECT *
            FROM items
            LEFT JOIN images
            ON items.item_pk = images.item_id
            AND images.image_deleted_at IS NULL
            WHERE items.item_created_by = %s
            AND items.item_deleted_at IS NULL
            ORDER BY items.item_created_at DESC
        """, (user_pk,))
        # Fetch the user's items
        user_items = cursor2.fetchall()
        cursor2.close(); db2.close()
        # Convert Decimal prices to float for JSON serialization
        for it in user_items:
            if isinstance(it.get("item_price"), Decimal):
                it["item_price"] = float(it["item_price"])

        # Render the profile template with an error message
        return render_template(
            "profile.html",
            title="Profile",
            x=x,
            user=session.get("user"),
            items=user_items,
            rates=rates,
            translate=languages.translate,
            lan=lan,
            delete_error=True
        ), 400

    # Soft delete - this will set user_deleted_at to NOW() and user_is_blocked to 1
    cursor.execute("""
        UPDATE users
        SET
        user_deleted_at = NOW(),
        user_is_blocked = 1
        WHERE user_pk = %s
    """, (user_pk,))
    db.commit()

    # Send a confirmation email to the user
    try:
        x.send_deletion_email(
            row["user_name"],
            row["user_last_name"],
            row["user_email"],
            lan=lan
        )
    except Exception as mail_ex:
        ic(f"Error sending deletion mail: {mail_ex}")

    cursor.close(); db.close()

    # Clear the session to log out the user
    session.clear()

    # Leave a toast message in the session to notify the user
    session["toast_message"] = languages.translate("Deletion email sent", lan)
    session["toast_status"]  = "ok"
    session["toast_ttl"]     = "4000"

    # Redirect to login, toast will now be shown
    return redirect(url_for("login", lan=lan))


# GET route for searching items
##############################
@app.get("/search")
def search():
    try:
        # Get the search query from the request arguments
        search_for = request.args.get("q", "").strip()
        db, cursor = x.db()

        # If the search query is empty, return an empty list
        # if not search for name and address
        q = """
        SELECT *,
        MATCH(item_name, item_address) AGAINST (%s IN BOOLEAN MODE) AS relevance
        FROM items
        LEFT JOIN images
        ON items.item_pk = images.item_id
        AND images.image_deleted_at IS NULL
        WHERE MATCH(item_name, item_address)
        AGAINST (%s IN BOOLEAN MODE)
        ORDER BY relevance DESC
        """
        # Execute the query with the search term
        cursor.execute(q, (f"{search_for}*", f"{search_for}*"))
        rows = cursor.fetchall()
        return rows
    # Handle exceptions that may occur during the database operations
    except Exception as ex:
        ic(ex)
        # If the exception is related to a missing page number, return an error
        return "x", 400