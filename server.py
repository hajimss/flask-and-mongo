from flask import Flask, Response, stream_with_context, redirect, url_for, request, render_template, session, flash
from datetime import timedelta, datetime
import pymongo
import dns
import motor
import json
import pandas as pd
from bson.objectid import ObjectId
import os
import sys

print(sys.path)

app = Flask(__name__)
#app.permanent_session_lifetime = timedelta(minutes=5)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

# connection to mongo

try:
    MONGO_URL = os.environ['MONGO_URL']
    print(MONGO_URL)
    client = pymongo.MongoClient(MONGO_URL)
    db = client.test

    client.server_info() # trigger if cannot connect to the db
except:
    print("ERROR - cannot connect to the DB")

###############################################
@app.route('/')
def gohome():
    return redirect(url_for('home'))

###############################################
@app.route('/getUsers', methods=['GET'])
def get_user():
    try:
        name = request.form['name']
        dbResponse = list(db.users.find({'name':name}))
        for user in dbResponse:
            user['_id'] = str(user['_id'])
        print(dbResponse)
        return Response(
            response=json.dumps(dbResponse),
            status=200,
            mimetype='application/json'
        )
        """
        return Response(
            response=json.dumps({
                "message":"got it!!!"
            }),
            status=200,
            mimetype='application/json'
        )
        """
    
    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({
                "message":"cannot get user"
            }),
            status=500,
            mimetype='application/json'
        )

###############################################
@app.route('/createuser', methods=['GET', 'POST', 'DELETE'])
def create_user():
    try:
        if request.method == 'POST':
            user = {"name": request.form["name"], 
                    "lastName": request.form["lastName"]
                    }
            dbResponse = db.users.insert_one(user)
            print(dbResponse.inserted_id)
            Response(
                response=json.dumps({
                    "message": "user created", 
                    "id":f"{dbResponse.inserted_id}",
                    "size":f"{dbResponse.__sizeof__}"
                    }),
                status=200,
                mimetype='application/json'
            )
            flash(f"A new user has been created!", "info")
            return redirect(url_for("create_user"))
        else:
            return render_template("createuser.html")

    except Exception as ex:
        print(ex)
        flash(f"Error: {ex}", "info")
        return redirect(url_for("home"))

###############################################

@app.route('/friends', methods=['GET', 'POST'])
def friends():
    if request.method == 'GET':
        rows = list(db.users.find())
        return render_template("friends.html", rows=rows)

@app.route('/deleteuser/<name>', methods=['POST', 'GET'])
def deleteuser(name):
    if request.method == 'GET':
        print(request.method)
        query = {"name": name}
        dbResponse = db.users.delete_one(query)
        print(dbResponse)
        flash(f"Your friend by the name of {name}, has been CANCELLED!")
        return redirect(url_for("friends"))

###############################################

@app.route("/home")
def home():
    return render_template("index.html")

###############################################

# args passed
@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return render_template("user.html", name=user)
    else:
        flash(f"You are not logged in", "info")
        return redirect(url_for("login"))

###############################################

@app.route("/admin")
def admin():
    # in url_for use the function name in a string
    return redirect(url_for("user", name="Hazim!"))

###############################################

@app.route("/login", methods=["GET", "POST"])
def login():
    print(request.method)
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user
        flash(f"Successfully logged in, Master {user}", "info")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash(f"Already logged in!", "info")
            return redirect(url_for("user"))
        return render_template("login.html")

###############################################

@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"You have been logged out, {user}!", "info")
    session.pop("user", None)
    return redirect(url_for("login"))

###############################################

@app.route("/journal", methods=['GET', 'POST'])
def journal(): 
    if "user" in session:
        if request.method == 'GET':
            posts = db.posts.find()
            return render_template("journal.html", posts=posts)    

        elif request.method == 'POST':
            t1 = datetime.now()
            full_date_time = t1.strftime("%d %B %Y, %H:%M:%S")
            post = {
                'content':request.form['content'],
                'date': t1,
                'full_date_time': full_date_time
            }
            dbResponse = db.posts.insert_one(post)
            print(dbResponse)
            flash("New post have been added", "info")
            return redirect(url_for("journal"))

    else:
        flash("You are not logged in")
        return redirect(url_for("home"))
###############################################

app.config["CSV_UPLOADS"] = "/Users/hajimss/Desktop/flask projects/flaskXmongo/flask-and-mongo/uploads"

@app.route("/upload_csv", methods=['GET','POST'])
def upload_csv():
    if request.method == 'POST':
        if request.files:
            t1 = datetime.now()
            full_date_time = t1.strftime("%d %B %Y, %H:%M:%S")
            csv_file = request.files["csv"]
            csv_name = request.files["csv"].filename
            # save file to mongo database

            csv_json = {
                'raw_csv':csv_file.read().decode("utf-8"),
                'name':csv_name,
                'date': t1,
                'full_date_time': full_date_time
            }
            #csv.save(os.path.join(app.config["CSV_UPLOADS"], csv.filename))
            #db.save_file(csv_name,csv_file)
            dbResponse = db.csv.save(csv_json)
            print(dbResponse)
            print("csv saved")
            redirect(request.url)
    elif request.method == "GET":
        files = list(db.csv.find())
        return render_template("upload_csv.html", files=files)
    return render_template("upload_csv.html")

###############################################

@app.route("/expand_csv/<csv>", methods=["GET", "POST"])
def expand_csv(csv):
    if request.method == "GET":
        csv_contents = db.csv.find_one({"name":csv})
        print(csv_contents)
        return render_template("expand_csv.html", contents=csv_contents["csv"])
    return render_template("expand_csv.html")

###############################################

#need help for pandas import

###############################################

if __name__ == '__main__':
    app.run(port=8080, debug=True)