"""Server for movie ratings app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, Movie
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

# Replace this with routes and view functions!
@app.route('/')
def index():
    """Display the homepage."""

    return render_template('homepage.html')

@app.route('/movies')
def all_movies():
    """Display all movies."""
    movies = crud.get_all_movies()

    return render_template("all_movies.html", movies=movies)

@app.route('/movies/<int:movie_id>')
def show_movie(movie_id):
    """Show details for a movie."""
    
    # next_movie_id = movie_id + 1 #TypeError (str and int)

    # Below: SQLAlchemy equality is True
    movie = crud.get_movie_by_id(movie_id)
    # print("#" * 100)
    # print(movie.movie_id == movie_id) #Python is False

    return render_template("movie_details.html", movie=movie)


@app.route('/users')
def all_users():
    """Display all users."""
    users = crud.get_all_users()

    return render_template("all_users.html", users=users)


@app.route('/users', methods=['POST'])
def create_account():
    """Create a new user account."""

    password = request.form.get('password')
    email = request.form.get('email')

    if crud.get_user_by_email(email) != None:
        flash('Email exists. Please sign up with a different email.')
    else:
        crud.create_user(email, password)
        flash('Account created successfully!')

    return redirect('/')


@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show details for a user"""
    user = crud.get_user_by_id(user_id)

    return render_template("user_details.html", user=user)

@app.route('/login', methods=['POST'])
def log_in_user():
    """Login user and redirect to homepage."""
    email = request.form.get('email')
    password = request.form.get('password')

    user_object = crud.get_user_by_email(email)

    if user_object != None:
        if password == user_object.password != None:
            session['user_id'] = user_object.user_id
            flash('Logged in!')
        else:
            flash('Incorrect password')   
    else:
        flash('Email does not exist. Please sign up above.')

    return redirect('/')

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
