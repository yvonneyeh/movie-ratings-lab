"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

# More code will go here
os.system('dropdb ratings')
os.system('createdb ratings')

model.connect_to_db(server.app)
model.db.create_all()

# Load movie data from JSON file
with open('data/movies.json') as f:
    movie_data = json.loads(f.read())

# Create movies, store them in list so we can use them
# to create fake ratings later
movies_in_db = []
for movie in movie_data:
    # Get the title, overview, and poster_path from the movie dictionary. 
    title = movie.get('title')
    overview = movie.get('overview')
    poster_path = movie.get('poster_path')

    # Get the release_date and convert it to a datetime object with datetime.strptime
    release_date = datetime.strptime(movie.get('release_date'), '%Y-%m-%d')
    
    # Create movie instances
    movie_obj = crud.create_movie(title, overview, release_date, poster_path)

    # Append movie object to movies_in_db list
    movies_in_db.append(movie_obj)

for n in range(10):
    email = f'user{n}@test.com'  # Voila! A unique email!
    password = 'test'

    new_user = crud.create_user(email, password)

    for _ in range(10):
        crud.create_rating(new_user, choice(movies_in_db), randint(1, 5))

###
# rating = Rating.query.first().user.ratings

# rating = Rating.query.first()
# ratings = rating.user.ratings

# for rating in ratings:
#     print(rating.score)