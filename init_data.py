from forms import *
from app import Genre, db

# if genres is empty, insert with some initial data
if not Genre.query.all():
  genres = [
    Genre(name='Alternative'),
    Genre(name='Blues'),
    Genre(name='Classical'),
    Genre(name='Country'),
    Genre(name='Electronic'),
    Genre(name='Folk'),
    Genre(name='Funk'),
    Genre(name='Hip-Hop'),
    Genre(name='Heavy Metal'),
    Genre(name='Instrumental'),
    Genre(name='Jazz'),
    Genre(name='Musical Theatre'),
    Genre(name='Pop'),
    Genre(name='Punk'),
    Genre(name='R&B'),
    Genre(name='Reggae'),
    Genre(name='Rock n Roll'),
    Genre(name='Soul'),
    Genre(name='Other')
  ]
  db.session.bulk_save_objects(genres)
  db.session.commit()
  print(f'The database has been initialized with genres')
else:
    print(f'Genres are already present in the database, Nothing is done')