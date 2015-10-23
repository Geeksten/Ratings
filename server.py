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


    user = User.query.filter_by(email=email).first()

    if user:
        flash("You're already a user. Please log in.")
        return redirect("/login")

    else:
        user = User(email=email, password=password)

        db.session.add(user)
        db.session.commit()

        return redirect("/users/%s" % user.user_id)

@app.route("/login")
def  login_form():
    """Have users login using email and password"""

    return render_template("login_form.html")


@app.route("/login_confirmation", methods=["POST"])
def login_confirmation():
    """Inform users that they logged in succesfully and provide a link to their profile"""

    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email=email, password=password).first()

    if user:
        session['user_id']=user.user_id
        # return redirect("/users/<int:user.user_id>")
        return redirect("/users/%s" % user.user_id)
    else:
        flash("Incorrect username or password")
        return redirect("/login")
    

@app.route("/users/<int:user_id>")
def show_user_profile(user_id):
    """"Return page showing the details of a given user."""

    user = User.query.filter_by(user_id=user_id).one()
    rating = Rating.query.filter_by(user_id=user_id).all()

    
    return render_template("user_detail.html", user=user, rating=rating)
  


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True
    app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False 

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
