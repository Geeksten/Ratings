"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the SQLite database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of ratings website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    zipcode = db.Column(db.String(15), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s email=%s>" % (self.user_id, self.email)


# Put your Movie and Rating model classes here.

class Movie(db.Model): #create an instance of this class which = Movie 
#when we say print it uses the repr function. 
    """Movies available for rating"""

    __tablename__ = "movies"

    movie_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    released_at = db.Column(db.DateTime, nullable=True) #datetime any date or time in this field
    imdb_url = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        """Provide helpful information about the movie."""

        return "<Movie movie_id=%s title=%s released_at=%s imdb_url=%s>" %(self.movie_id, 
                                                                            self.title,
                                                                            self.released_at,
                                                                            self.imdb_url)
#Now we add the Rating model class:
class Rating(db.Model):
    """Ratings for movies in our website"""

    __tablename__="ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    #The column below is still an integer, but we’re also declaring it to be a ForeignKey,
    #which is just a fancy way of saying it references another column in another table. 
    #The parameter passed to ForeignKey() should be a string in the format of “table.column_name”. 
    #Here, we’re saying that the movie_id column of the ratings table refers to the movie_id column 
    #of the movie table:
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'))
    #The column below is still an integer, but we’re also declaring it to be a ForeignKey,
    #which is just a fancy way of saying it references another column in another table. 
    #The parameter passed to ForeignKey() should be a string in the format of “table.column_name”. 
    #Here, we’re saying that the user_id column of the ratings table refers to the user_id column 
    #of the users table:

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    score = db.Column(db.Integer)

    #Define relationship to user:
    #This line establishes a relationship between the Rating and User objects, along with backref. 
    #The relationship adds an attribute on ratings objects called user. This value of this attribute is the same 
    #object as if you had queried the database directly for that user.On a user object, there is an attribute named ratings. 
    #This attribute is a list of all the ratings associated with that user, simultaneously queried from the database.
    #The relationship attribute defined on the Rating class just tells SQLAlchemy how it should construct the JOIN clause of 
    #its SELECT statement. It then takes all the results and turns them into the correct objects.
    #Note that these relationship attributes don’t change the actual tables – the data stored in the ratings table is still the 
    #integer movie_id and user_id fields, for example. These movie and user relationship attributes 
    #added to the Rating class provide a quick and convenient way to get to the related movie and user objects, respectively.
    user = db.relationship("User",
                           backref=db.backref("ratings", order_by=rating_id))

    #Define relationship to movie
    movie = db.relationship("Movie",
                            backref=db.backref("ratings", order_by=rating_id))
    def __repr__(self):
        """Provide helpulful information about the ratings a user gave."""
        
        return "<Rating rating_id=%s movie_id=%s user_id=%s score=%s>" % (self.rating_id, 
                                                                        self.movie_id,
                                                                        self.user_id,
                                                                        self.score)
        #syntax we use to show that it is a rating object

##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ratings.db'
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
 