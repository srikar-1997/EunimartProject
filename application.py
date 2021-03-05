import os
import datetime
from models import *

from flask import Flask, session, render_template, request, redirect, url_for, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import logging
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc, or_, and_
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config.from_object(__name__)
Session(app)

app.config["TEMPLATES_AUTO_RELOAD"] = True

engine = create_engine(os.getenv("DATABASE_URL"))
db1 = scoped_session(sessionmaker(bind=engine))



@app.route("/")
def index():
    if 'email' not in session :
        return redirect(url_for('register'))
    elif session['email'] :
        rows = db1.execute(f"SELECT * FROM candidates")
        dic = {}
        for row in rows:
            # print(row.id)
            # print(row.candidatename)
            dic[row.id] = [row.candidatename, row.no_of_votes]
        if Users.query.get(session['email']).type  == "Admin":
            return render_template("home.html", dic = dic, flag = 1)
        else:
            return render_template("home.html", dic = dic, flag_1 = 1)

@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for('register'))

@app.route("/register", methods = ["GET", "POST"] )
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        email = request.form.get("email").lower()
        password = request.form.get("password")
        conf_password = request.form.get("confirmation")
        
        if password != conf_password:
            return render_template("register.html", flag = 1)
        hash = generate_password_hash(password)
        reg = Users(email = email, hash = hash, isVoted= False, type = "user")
        try:
            db.session.add(reg)
            db.session.commit()
            return redirect(url_for('login'))
        except exc.IntegrityError:
            return render_template("register.html", flag_1 = 1)
        except:
            print('exception message', 'something went wrong in adding user')


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email').lower()
        # Query database for username
        rows = Users.query.get(email)
        
        # Ensure username exists and password is correct
        if rows is None:
            return render_template("login.html", flag= 1)
        if not check_password_hash(rows.hash, request.form.get("password")):
            return render_template("login.html", flag_1= 1)
        if rows.isVoted:
            return render_template("login.html", flag_2= 1)
        # Remember which user has logged in
        session["email"] = email

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
    
    
@app.route("/vote", methods=["POST"])
def vote():
    data = request.get_json()
    id = request.form.get('value')
    cand_data = Candidates.query.get(id)
    user_data = Users.query.get(session['email'])
    user_data.isVoted = True
    cand_data.no_of_votes += 1
    db.session.add(user_data)
    db.session.add(cand_data)
    db.session.commit()
    return jsonify({"success": True, "status":"200"})
