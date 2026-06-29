from flask import Flask, render_template,request,redirect,url_for,flash,session
from dotenv import load_dotenv
import os
import mysql.connector

from DB import(
    create_database,
    create_tables,
    insert_user,
    login_user,    
)

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY", "trinetra_ai_secret_2026")






# ================= HOME PAGE =================
@app.route("/")
def home():
    return render_template("index.html")

# ================= Reagistration PAGE =================

@app.route("/registration", methods=["GET","POST"])

def registration():
    
    if request.method == "POST":
        
        full_name = request.form["full_name"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        mobile = request.form["mobile"]
        state = request.form["state"]
        district = request.form["district"]
        village = request.form["village"]
        language = request.form["language"]
       
        
        if password != confirm_password:
            flash("Password do not match.")
            return redirect(url_for("registration"))
        
        try:
            insert_user(

                full_name,
                email,
                mobile,
                password,
                state,
                district,
                village,
                language
            )
            
            user = login_user(email, password)
            if user:
                
             session["user_id"] = user["id"]
             session["user_name"] = user["full_name"]
            
            flash("Registration Successful.")
            
            return redirect(url_for("home1"))
        
        except Exception as e:
            
            print(e)
            flash (str(e))
        
    return render_template("register.html")


# ==========================================
# LOGIN
# ==========================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]

        password = request.form["password"]

        user = login_user(email, password)

        if user:

            session["user_id"] = user["id"]

            session["user_name"] = user["full_name"]

            return redirect(url_for("home1"))

        flash("Invalid Email or Password.")

        return redirect(url_for("login"))
    return render_template("login.html")

# ==========================================
# HOME
# ==========================================

@app.route("/home")
def home1():

    if "user_id" not in session:

        return redirect(url_for("login"))

    return render_template(

        "dashboard.html",

        user_name=session["user_name"]

    )
    
# ==========================================
# LOGOUT
# ==========================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("home"))


# ==========================================
# RUN APP
# ==========================================

if __name__ == "__main__":
    
    app.run(
        debug=True
    )

