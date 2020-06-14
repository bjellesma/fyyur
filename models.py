from app import db

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

venue_genre = db.Table(
  'venue_genre',
  db.Column('venue_id', db.Integer, db.ForeignKey('venue.id'), primary_key=True),
  db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'), primary_key=True)
)
venue_show = db.Table(
  'venue_show',
  db.Column('venue_id', db.Integer, db.ForeignKey('venue.id'), primary_key=True),
  db.Column('show_id', db.Integer, db.ForeignKey('show.id'), primary_key=True)
)
artist_genre = db.Table(
  'artist_genre',
  db.Column('artist_id', db.Integer, db.ForeignKey('artist.id'), primary_key=True),
  db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'), primary_key=True)
)
artist_show = db.Table(
  'artist_show',
  db.Column('artist_id', db.Integer, db.ForeignKey('artist.id'), primary_key=True),
  db.Column('show_id', db.Integer, db.ForeignKey('show.id'), primary_key=True)
)

class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    website = db.Column(db.String(500))
    facebook_link = db.Column(db.String(500))
    image_link = db.Column(db.String(500))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String)
    shows = db.relationship('Show', secondary=venue_show, backref='venue', lazy=True)
    genres = db.relationship('Genre', secondary=venue_genre, backref='venue', lazy=True)

class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

class Show(db.Model):
    __tablename__ = 'show'
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable = False)
    # There are no relationships established to delete artists or venues if we delete a show
    # This is a rare instance on a one to one relationship
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)


class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(500))
    facebook_link = db.Column(db.String(500))
    image_link = db.Column(db.String(500))
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String)
    shows = db.relationship('Show', secondary=artist_show, backref='artist', lazy=True)
    genres = db.relationship('Genre', secondary=artist_genre, backref='artist', lazy=True)
