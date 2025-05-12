from flask import Flask, render_template, session, request, redirect, url_for, abort
from werkzeug.security import generate_password_hash, check_password_hash
# admin_hash = generate_password_hash("admin")
from flask_session import Session
from decimal import Decimal
from datetime import datetime, date
import x
import time
import uuid
import os
import json
import languages
import requests
import traceback

app = Flask(__name__)

from icecream import ic
ic.configureOutput(prefix=f'----- | ', includeContext=True)

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


# Til login/log ud men virker umiddelbart uden?
##############################
@app.context_processor
def inject_user():
    # makes `user` available in every template
    return {"user": session.get("user")}


##############################
@app.context_processor
def utility_processor():
    def image_path(filename):
        """Returner den korrekte static-sti til billedet."""
        # Absolutte stier til de to mulige mapper
        upload_fp = os.path.join(app.static_folder, "uploads", filename)
        image_fp  = os.path.join(app.static_folder, "images", filename)

        # Tjek hvad der findes
        if os.path.isfile(upload_fp):
            folder = "uploads"
        elif os.path.isfile(image_fp):
            folder = "images"
        else:
            folder = "uploads"   # eller 'images', fallback hvis ingen findes

        return url_for("static", filename=f"{folder}/{filename}")

    return dict(image_path=image_path)











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
        data = requests.get("https://open.er-api.com/v6/latest/USD")
        ic(data.json())
        with open("rates.txt", "w") as file:
            file.write(data.text)
        return data.json()
    except Exception as ex:
        ic(ex)


##############################
@app.get("/")
@app.get("/<lan>/")
def index(lan="dk"):
    user = session.get("user")
    if lan not in languages.translations:
        lan = "dk"
    try:
        db, cursor = x.db()
        # languages_allowed = ["dk", "en"]
        # if lan not in languages_allowed: lan = "dk"
        q = """
        SELECT *
        FROM items
        LEFT JOIN images
        ON items.item_pk = images.item_id
        AND images.image_slot = 1
        AND images.image_deleted_at IS NULL
        ORDER BY items.item_created_at DESC
        LIMIT 2
        """
        cursor.execute(q)
        items = cursor.fetchall()

##
        for it in items:
            if isinstance(it.get("item_price"), Decimal):
                it["item_price"] = float(it["item_price"])



        rates = ""
        with open("rates.txt", "r") as file:
            rates = file.read() # this is text that looks like json
        ic(rates)
        # Convert the text rates to json
        rates = json.loads(rates)
        return render_template("index.html", title="Vejhylden", items=items, rates=rates, translate=languages.translate, lan=lan, user=user)
    except Exception as ex:
        ic(ex)
        return "ups"
    finally:
        pass


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


##############################
@app.post("/signup")
@app.post("/<lan>/signup")
def post_signup(lan="dk"):
    try:
        user_username = x.validate_user_username()
        user_name = x.validate_user_name()
        user_last_name = x.validate_user_last_name()
        user_email = x.validate_user_email()
        user_password = x.validate_user_password()
        hashed_password = generate_password_hash(user_password)
        # ic(hashed_password)

        q = """INSERT INTO users 
        (user_username, user_name, user_last_name, user_email, 
        user_password) 
        VALUES (%s, %s, %s, %s, %s)"""

        db, cursor = x.db()
        cursor.execute(q, (user_username, user_name, user_last_name, user_email, hashed_password,))

        if cursor.rowcount != 1: raise Exception("System under maintenance")

        db.commit()



        try:
            x.send_email(user_name, user_last_name, user_email)
        except Exception as mail_ex:
            ic(f"Email-fejl: {mail_ex} (brugeren er oprettet)")


        return redirect(url_for("login", message="Signup ok", lan=lan))
    except Exception as ex:
        ic(ex)
        traceback.print_exc()
        if "db" in locals(): db.rollback()
        # request.form is a tuple
        # test = request.form
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
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()



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


# fra full 15
##############################
@app.post("/login")
@app.post("/<lan>/login")
def post_login(lan="dk"):
    try:
        # MUST VALIDATE
        user_email = x.validate_user_email()
        user_password = x.validate_user_password()

        db, cursor = x.db()
        q = """
        SELECT user_pk, user_name, user_last_name, user_password, user_is_admin FROM users WHERE user_email = %s AND user_deleted_at IS NULL
        """
        cursor.execute(q, (user_email,))
        user = cursor.fetchone()
        if not user:
            raise Exception("User not found")





        # db, cursor = x.db()
        # q = "SELECT * FROM users WHERE user_email = %s"
        # cursor.execute(q, (user_email,))
        # user = cursor.fetchone()
        # if not user: raise Exception("User not found")



        if not check_password_hash(user["user_password"], user_password):
            raise Exception("Invalid credentials")
        # todo: remove the user's password
        user.pop("user_password")
        ic(user)
        session["user"] = user


        if user.get("user_is_admin"):
            return redirect(url_for("admin", lan=lan))
        else:
            return redirect(url_for("profile", lan=lan))

    except Exception as ex:
        ic(ex)
        return str(ex), 400

    finally:
        if "cursor" in locals(): cursor.close()
        if "db"     in locals(): db.close()





    #     return redirect(url_for("profile"))
    # except Exception as ex:
    #     ic(ex)
    #     return str(ex), 400 
    # finally:
    #     if "cursor" in locals(): cursor.close()
    #     if "db" in locals(): db.close()  


##############################
@app.get("/admin")
@app.get("/<lan>/admin")
def admin(lan="dk"):
    user = session.get("user")
    # only allow real admins
    if not user or not user.get("user_is_admin"):
        return abort(403)

    try:
        db, cursor = x.db()

        # ── 1) Handle toggles ──
        toggle_item = request.args.get("toggle_item")
        if toggle_item:
            cursor.execute(
                "UPDATE items SET item_is_blocked = NOT item_is_blocked WHERE item_pk = %s",
                (toggle_item,)
            )
            db.commit()

        toggle_user = request.args.get("toggle_user")
        if toggle_user:
            cursor.execute(
                "UPDATE users SET user_is_blocked = NOT user_is_blocked WHERE user_pk = %s",
                (toggle_user,)
            )
            db.commit()

        # ── 2) Fetch single item (if needed) ──
        cursor.execute("""
            SELECT *
            FROM items
            LEFT JOIN images
              ON items.item_pk = images.item_id
              AND images.image_slot = 1
              AND images.image_deleted_at IS NULL
            WHERE items.item_pk = %s
        """, (toggle_item,))
        items = cursor.fetchone()

        # ── 3) Fetch all items ──
        q_items = """
        SELECT *
        FROM items
        LEFT JOIN images
          ON items.item_pk = images.item_id
          AND images.image_slot = 1
          AND images.image_deleted_at IS NULL
        ORDER BY items.item_created_at DESC
        """
        cursor.execute(q_items)
        items = cursor.fetchall()

        # ── 4) Fetch all users ──
        q_users = "SELECT * FROM users ORDER BY user_created_at DESC"
        cursor.execute(q_users)
        users = cursor.fetchall()

        # ── 5) Convert Decimal prices to float ──
        for it in items:
            if isinstance(it.get("item_price"), Decimal):
                it["item_price"] = float(it["item_price"])

        # ── 6) Load rates ──
        with open("rates.txt", "r") as file:
            rates = json.loads(file.read())

        # ── 7) Render template ──
        return render_template(
            "admin.html",
            title="Admin",
            items=items,
            rates=rates,
            user=user,
            users=users,
            x=x,
            translate=languages.translate,
            lan=lan
        )

    except Exception as ex:
        ic(ex)
        return "ups"
    finally:
        pass



















##############################
# @app.get("/admin")
# @app.get("/<lan>/admin")
# def admin(lan="dk"):
#     user = session.get("user")
#     # only allow real admins
#     if not user or not user.get("user_is_admin"):
#         return abort(403)
#     try:
#         db, cursor = x.db()


#         toggle_item = request.args.get("toggle_item")
#         if toggle_item:
#             cursor.execute(
#                 "UPDATE items SET item_is_blocked = NOT item_is_blocked WHERE item_pk = %s",
#                 (toggle_item,)
#             )
#             db.commit()
        

#         cursor.execute("""
#                 SELECT *
#                 FROM items
#                 LEFT JOIN images
#                 ON items.item_pk = images.item_id
#                 AND images.image_slot = 1
#                 AND images.image_deleted_at IS NULL
#                 WHERE items.item_pk = %s
#             """, (toggle_item,))
#         items = cursor.fetchone()


        
#         # languages_allowed = ["dk", "en"]
#         # if lan not in languages_allowed: lan = "dk"
#         # q = "SELECT * FROM items ORDER BY item_created_at"
#         q_items = """
#         SELECT *
#         FROM items
#         LEFT JOIN images
#         ON items.item_pk = images.item_id
#         AND images.image_slot = 1
#         AND images.image_deleted_at IS NULL
#         ORDER BY items.item_created_at DESC
#         """
#         cursor.execute(q_items)
#         items = cursor.fetchall()



#         toggle_user = request.args.get("toggle_user")
#         if toggle_user:
#             cursor.execute(
#                 "UPDATE users SET user_is_blocked = NOT user_is_blocked WHERE user_pk = %s",
#                 (toggle_user,)
#             )
#             db.commit()
        


#         q_users = "SELECT * FROM users ORDER BY user_created_at DESC"
    
#         cursor.execute(q_users)
#         users = cursor.fetchall()

# ##
#         for it in items:
#             if isinstance(it.get("item_price"), Decimal):
#                 it["item_price"] = float(it["item_price"])

#         rates = ""
#         with open("rates.txt", "r") as file:
#             rates = file.read() # this is text that looks like json
#         ic(rates)
#         # Convert the text rates to json
#         rates = json.loads(rates)
#     # render your admin.html template
#         return render_template("admin.html", title="Admin", items=items, rates=rates, user=user, users=users, x=x, translate=languages.translate, lan=lan)
#     except Exception as ex:
#         ic(ex)
#         return "ups"
#     finally:
#         pass

##############################
# @app.get("/admin")
# @app.get("/<lan>/admin")
# def admin(lan="dk"):
#     user = session.get("user")
#     # only allow real admins
#     if not user or not user.get("is_admin"):
#         return abort(403)
#     # render your admin.html template
#     return render_template("admin.html", title="Admin", user=user, x=x, translate=languages.translate, lan=lan)


##############################
@app.get("/profile")
@app.get("/<lan>/profile")
def profile(lan="dk"):
    user = session.get("user")
    return render_template("profile.html", title="Profile", x=x, user=user, translate=languages.translate, lan=lan)

# MANGLER LANGUAGE
##############################
@app.get("/logout")
@app.get("/<lan>/logout")
def logout(lan="dk"):
    session.pop("user")
    return redirect(url_for("login", lan=lan))


##############################
@app.get("/items/<item_pk>")
@app.get("/<lan>/items/<item_pk>")
def get_item_by_pk(item_pk):
    lan = request.args.get('lan', 'dk')
    if lan not in ("dk","en"):
        lan = "dk"
    try:
        db, cursor = x.db()
        # q = "SELECT * FROM items WHERE item_pk = %s"
        q = """
        SELECT *
        FROM items
        LEFT JOIN images
        ON items.item_pk = images.item_id
        AND images.image_slot = 1
        AND images.image_deleted_at IS NULL
        WHERE items.item_pk = %s
    """

        cursor.execute(q, (item_pk,))
        item = cursor.fetchone()

###
        if item and isinstance(item.get("item_price"), Decimal):
            item["item_price"] = float(item["item_price"])




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



##############################
@app.get("/items/page/<page_number>")
@app.get("/<lan>/items/page/<page_number>")
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
        # q = "SELECT * FROM items ORDER BY item_created_at LIMIT %s OFFSET %s"

        q = """
        SELECT *
        FROM items
        LEFT JOIN images
        ON items.item_pk = images.item_id
        AND images.image_slot = 1
        AND images.image_deleted_at IS NULL
        ORDER BY items.item_created_at DESC
        LIMIT %s OFFSET %s
        """
        cursor.execute(q, (extra_item, offset))
        items = cursor.fetchall()


###
        for it in items:
            for k, v in list(it.items()):
                if isinstance(v, Decimal):
                    it[k] = float(v)
                elif isinstance(v, (datetime, date)):
                    it[k] = v.isoformat()


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


##############################
@app.post("/item")
@app.post("/<lan>/item")
def create_item(lan="dk"):
    # 1) Tjek at brugeren er logget ind
    user = x.validate_user_logged()

    # 2) Valider og hent de øvrige formular-felter
    item_name    = request.form["item_name"].strip()
    item_address = request.form["item_address"].strip()
    item_price   = request.form["item_price"].strip()

    # 3) Geokodér adressen (som før)
    try:
        resp = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": item_address, "format": "json"},
            headers={"User-Agent": "my-flask-app/1.0"}
        )
        data = resp.json()
        latitude  = float(data[0]["lat"]) if data else 0.0
        longitude = float(data[0]["lon"]) if data else 0.0
    except:
        latitude = longitude = 0.0

    # 4) Opdel billed-validering & gemning til x.validate_item_images()
    #    Den returnerer en liste af nye filnavne
    image_filenames = x.validate_item_images()[:3]

    # 5) Indsæt item i DB
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
    db.commit()

    # 6) Gem de validerede billeder i images-tabellen
    for slot, fname in enumerate(image_filenames, start=1):
        cursor.execute(
            "INSERT INTO images (item_id,item_image,image_slot) VALUES (%s,%s,%s)",
            (item_pk, fname, slot)
        )
    db.commit()

    cursor.close()
    db.close()

    return redirect(url_for("profile", lan=lan))













##############################
##############################
##############################
@app.get("/users/<user_pk>")
@app.get("/<lan>/users/<user_pk>")
def get_user_by_pk(user_pk, lan="dk"):
    lan = request.args.get('lan', 'dk')
    if lan not in ("dk","en"):
        lan = "dk"
    try:
        db, cursor = x.db()
        q = "SELECT * FROM users WHERE user_pk = %s"

        cursor.execute(q, (user_pk,))
        user = cursor.fetchone()

        rates= ""
        with open("rates.txt", "r") as file:
            rates = file.read() # this is text that looks like json
            rates = json.loads(rates)

        html_user = render_template("_admin_user.html", user=user, lan=lan,                   
            translate=languages.translate)
        return f"""
            <mixhtml mix-replace="#user">
                {html_user}
            </mixhtml>
        """
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



##############################
@app.get("/search")
def search():
    try:
        search_for = request.args.get("q", "").strip() # car
        # TODO: validate search_for
        db, cursor = x.db()
        # q = "SELECT * FROM items WHERE item_name LIKE %s"
        q = """
        SELECT *
        FROM items
        LEFT JOIN images
        ON items.item_pk = images.item_id
        AND images.image_slot = 1
        AND images.image_deleted_at IS NULL
        WHERE items.item_name LIKE %s
        """
        cursor.execute(q, (f"{search_for}%",))
        rows = cursor.fetchall()
        ic(rows)
        return rows # [{'item_name': 'aa1', 'item_pk': '193e055791ed4f...
    except Exception as ex:
        ic(ex)
        return "x", 400

