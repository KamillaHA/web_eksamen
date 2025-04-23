from flask import Flask, render_template, session, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session
import x
import time
import uuid
import os
import json
import languages
import requests

app = Flask(__name__)

from icecream import ic
ic.configureOutput(prefix=f'----- | ', includeContext=True)

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


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


##############################
@app.get("/rates")
def get_rates():
    try:
        data = requests.get("https://api.exchangerate-api.com/v4/latest/usd")
        ic(data.json())
        with open("rates.txt", "w") as file:
            file.write(data.text)
        return data.json()
    except Exception as ex:
        ic(ex)


##############################
@app.get("/")
@app.get("/<lan>")
def index(lan="dk"):
    if lan not in languages.translations:
        lan = "dk"
    try:
        db, cursor = x.db()
        # languages_allowed = ["dk", "en"]
        # if lan not in languages_allowed: lan = "dk"
        q = "SELECT * FROM items ORDER BY item_created_at LIMIT 2"
        cursor.execute(q)
        items = cursor.fetchall()
        rates = ""
        with open("rates.txt", "r") as file:
            rates = file.read() # this is text that looks like json
        ic(rates)
        # Convert the text rates to json
        rates = json.loads(rates)
        return render_template("index.html", title="Vejhylden", items=items, rates=rates, translate=languages.translate, lan=lan)
    except Exception as ex:
        ic(ex)
        return "ups"
    finally:
        pass


##############################
@app.get("/signup")
def signup():
    try:
        return render_template("signup.html", title="Signup", x=x)
    except Exception as ex:
        ic(ex)
        return "error loading signup page"
    finally:
        pass


##############################
@app.post("/signup")
def post_signup():
    try:
        user_username = x.validate_user_username()
        user_name = x.validate_user_name()
        user_last_name = x.validate_user_last_name()
        user_email = x.validate_user_email()
        user_password = x.validate_user_password()
        hashed_password = generate_password_hash(user_password)
        # ic(hashed_password)
        user_created_at = int(time.time())

        q = """INSERT INTO users 
        (user_pk, user_username, user_name, user_last_name, user_email, 
        user_password, user_created_at, user_updated_at, user_deleted_at) 
        VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s)"""

        db, cursor = x.db()
        cursor.execute(q, (user_username, user_name,user_last_name,user_email,hashed_password,user_created_at,0,0))

        if cursor.rowcount != 1: raise Exception("System under maintenance")

        db.commit()
        x.send_email(user_name, user_last_name)
        return redirect(url_for("login", message="Signup ok"))
    except Exception as ex:
        ic(ex)
        if "db" in locals(): db.rollback()
        # request.form is a tuple
        # test = request.form
        old_values = request.form.to_dict()
        if "username" in str(ex):
            old_values.pop("user_username", None)
            return render_template("signup.html",                                   
                error_message="Invalid username", old_values=old_values, user_username_error="input_error")
        if "first name" in str(ex):
            old_values.pop("user_name", None)
            return render_template("signup.html",
                error_message="Invalid name", old_values=old_values, user_name_error="input_error")
        if "last name" in str(ex):
            old_values.pop("user_last_name", None)
            return render_template("signup.html",
                error_message="Invalid last name", old_values=old_values, user_last_name_error="input_error")
        if "Invalid email" in str(ex):
            old_values.pop("user_email", None)
            return render_template("signup.html",
                error_message="Invalid email", old_values=old_values, user_email_error="input_error")
        if "password" in str(ex):
            old_values.pop("user_password", None)
            return render_template("signup.html",
                error_message="Invalid password", old_values=old_values, user_password_error="input_error")

        if "user_email" in str(ex):
            return redirect(url_for("signup",
                error_message="Email already exists", old_values=old_values, email_error=True))
        if "user_username" in str(ex): 
            return redirect(url_for("signup", 
                error_message="Username already exists", old_values=request.form, user_username_error=True))
        return redirect(url_for("signup", error_message=ex.args[0]))
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()



##############################
@app.get("/login")
def login():
    try:
        return render_template("login.html", title="Login", x=x)
    except Exception as ex:
        ic(ex)
        return "error loading login page"
    finally:
        pass


# fra full 15
##############################
@app.post("/login")
def post_login():
    try:
        # MUST VALIDATE
        user_email = x.validate_user_email()
        user_password = x.validate_user_password()
        db, cursor = x.db()
        q = "SELECT * FROM users WHERE user_email = %s"
        cursor.execute(q, (user_email,))
        user = cursor.fetchone()
        if not user: raise Exception("User not found")
        if not check_password_hash(user["user_password"], user_password):
            raise Exception("Invalid credentials")
        # todo: remove the user's password
        user.pop("user_password")
        ic(user)
        session["user"] = user
        return redirect(url_for("profile"))
    except Exception as ex:
        ic(ex)
        return str(ex), 400 
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()  


##############################
@app.get("/profile")
def profile():
    return render_template("profile.html", title="Profile", x=x)


##############################
@app.get("/logout")
def logout():
    session.pop("user")
    return redirect(url_for("login"))


##############################
@app.get("/items/<item_pk>")
def get_item_by_pk(item_pk):
    lan = request.args.get('lan', 'dk')
    if lan not in ("dk","en"):
        lan = "dk"
    try:
        db, cursor = x.db()
        q = "SELECT * FROM items WHERE item_pk = %s"
        cursor.execute(q, (item_pk,))
        item = cursor.fetchone()

        rates= ""
        with open("rates.txt", "r") as file:
            rates = file.read() # this is text that looks like json
            rates = json.loads(rates)

        html_item = render_template("_item.html", item=item, rates=rates, lan=lan,                   
            translate=languages.translate)
        return f"""
            <mixhtml mix-replace="#item">
                {html_item}
            </mixhtml>
        """
    except Exception as ex:
        ic(ex)
        if "web_ex page number" in str(ex):
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



##############################
@app.get("/items/page/<page_number>")
def get_items_by_page(page_number):
    lan = request.args.get('lan', 'dk')
    if lan not in ("dk","en"):
        lan = "dk"
    try:
        page_number = x.validate_page_number(page_number)
        items_per_page = 2
        offset = (page_number-1) * items_per_page
        extra_item = items_per_page + 1
        db, cursor = x.db()
        q = "SELECT * FROM items ORDER BY item_created_at LIMIT %s OFFSET %s"
        cursor.execute(q, (extra_item, offset))
        items = cursor.fetchall()
        html = ""
        
        rates= ""
        with open("rates.txt", "r") as file:
            rates = file.read() # this is text that looks like json
            rates = json.loads(rates)

        for item in items[:items_per_page]:
            i = render_template("_card.html", item=item, rates=rates, lan=lan, translate=languages.translate)
            html += i
        button = render_template("_btn_more_items.html", page_number=page_number + 1, lan=lan, translate=languages.translate)
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
    except Exception as ex:
        ic(ex)
        if "web_ex page number" in str(ex):
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



##############################
@app.get("/search")
def search():
    try:
        search_for = request.args.get("q", "") # car
        # TODO: validate search_for
        db, cursor = x.db()
        q = "SELECT * FROM items WHERE item_name LIKE %s"
        cursor.execute(q, (f"{search_for}%",))
        rows = cursor.fetchall()
        ic(rows)
        return rows # [{'item_name': 'aa1', 'item_pk': '193e055791ed4f...
    except Exception as ex:
        ic(ex)
        return "x", 400

