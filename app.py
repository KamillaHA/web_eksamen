from flask import Flask, render_template, session, request
from flask_session import Session
import x
import uuid

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
@app.get("/")
def index():
    try:
        db, cursor = x.db()
        q = "SELECT * FROM items ORDER BY item_name LIMIT 2"
        cursor.execute(q)
        items = cursor.fetchall()
        return render_template("index.html", title="Vejhylden", items=items)
    except Exception as ex:
        ic(ex)
        return "ups"
    finally:
        pass


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


##############################
@app.post("/login")
def post_login():
    try:
        email = x.validate_email()
        db, cursor = x.db()
        q = "SELECT * FROM users WHERE user_email = %s AND user_deleted_at = 0"
        cursor.execute(q, (email,))
        user = cursor.fetchone()
        if not user: raise Exception("web_ex user not found")
        ic(user)
        session["user"] = user
        return """
            <mixhtml mix-redirect="/profile">
            </mixhtml>
        """
    except Exception as ex:
        ic(ex)
        if "web_ex email" in str(ex):
            return """
                <mixhtml mix-top="body">
                    email invalid
                </mixhtml>
            """
        if "web_ex user not found" in str(ex):
            return """
                <mixhtml mix-top="body">
                    user not found
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