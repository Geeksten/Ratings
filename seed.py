"""Utility file to seed ratings database from MovieLens data in seed_data/"""


from model import User
from model import Rating
from model import Movie

from model import connect_to_db, db
from server import app
from datetime import datetime


def load_users():
    """Load users from u.user into database."""

    print "Users"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/u.user"):
        row = row.rstrip()
        user_id, age, gender, occupation, zipcode = row.split("|")

        user = User(user_id=user_id,
                    age=age,
                    zipcode=zipcode)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

    # Once we're done, we should commit our work
    db.session.commit()


def load_movies():
    """Load movies from u.item into database."""
    print "Movies"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Movie.query.delete()

    # Read u.item file and insert data
    for row in open("seed_data/u.item"):
        row =row.rstrip()

        movie_id, title_long, released_string, imdb_url = row.split("|")[:4]
        #we modified the datetime format changed released_string into 
        #new format by using datetim.strptime to convert it. 
        print row
        if released_string: 
            release_at = datetime.strptime(released_string, "%d-%b-%Y")
        else: 
            release_at = None 

        #here we stripped the title of the (xxxx) year and parenthesis
        #using the slice method. 
        title = title_long[:-7]

        print movie_id, title_long, released_string, imdb_url

        #assign the return values from our for loop to a new variable
        movie = Movie(movie_id=movie_id, title=title, released_at=release_at,
                      imdb_url=imdb_url)
    
        # We need to add to the session or it won't ever be stored
        db.session.add(movie)

    #Once we're done, we should commit our work
    db.session.commit()


def load_ratings():
    """Load ratings from u.data into database."""

    print "Ratings"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Rating.query.delete()

    # Read u.data file and insert data
    for row in open("seed_data/u.data"):
        row = row.rstrip()
        user_id, movie_id, score, timestamp = row.split("\t")

        user_id = int(user_id)
        movie_id = int(movie_id)
        score = int(score)

        #from rating class take the movie_id and make it equal to the movie_id 
        #from the for loop above. We are calling it to make an instance of the rating
        #class
        rating = Rating(movie_id=movie_id, user_id=user_id, score=score)
       
        #We need to add to the session or it won't ever be stored
        db.session.add(rating)

    #Once we're done, we should commit our work
    db.session.commit()

def make_new_user







if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    #load_users()
    #load_movies()
    #load_ratings()
