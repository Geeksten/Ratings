"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db



app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route("/new_user")
def new_users():
    """New user sign in form"""

    return render_template("new_user.html")

@app.route("/user_confirmation", methods=["POST"])
def user_confirmation():
    """This confirms new user has been added to our system."""

    email = request.form['email']
    password = request.form['password']

    print email, password

    user_name = User.query.filter_by(email=email).first()

    print user_name
    type(user_name)


    if (user_name==None):
        user = User(email=email, password=password)

        db.session.add(user)
      
        db.session.commit()
    else: 
        print "You are already a user please sign in."

    return render_template("user_confirmation.html")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()

    