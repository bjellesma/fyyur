from app import app
import json
import dateutil.parser
from datetime import datetime
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort
from logging import Formatter, FileHandler
from flask_wtf import FlaskForm
from forms import ShowForm, VenueForm, ArtistForm, SelectField, DataRequired
from models import *
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

#----------------------------------------------------------------------------#
# Utils
#----------------------------------------------------------------------------#

def str_to_bool(string_value):
  """
  takes a string value and converts it to a boolean object
  """
  if string_value and (string_value.lower() == 'y' or string_value.lower() == "on"):
    return True
  return False

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  data = []
  areas = db.session.query(Venue.city, Venue.state, db.func.count(Venue.id)).group_by(Venue.city, Venue.state).all()
  for city, state, venue_count in areas:
      venues = Venue.query.filter(Venue.city == city).all()
      data.append({
          'city': city,
          'state': state,
          'venue_count': venue_count,
          'venues': [{
              "id": venue.id,
              "name": venue.name
          } for venue in venues]
      })
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
    search_term = request.form.get('search_term')
    venues = Venue.query.with_entities(Venue.id, Venue.name).filter(Venue.name.ilike(f'%{search_term}%')).all()
    data = []
    for venue in venues:
        shows = Show.query.filter(db.and_(Show.venue_id==venue.id, Show.start_time > datetime.now())).count()
        data.append({
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": shows
        })
    response = {
        'count': len(venues),
        'data': data 
    }
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/<int:venue_id>', methods=['GET'])
def show_venue(venue_id):
    venue = Venue.query.get(venue_id)
    if not venue:
        abort(404)
    shows = Show.query.filter(Show.venue_id==venue.id).all()
    upcoming_shows = []
    past_shows = []
    for show in shows:
        if show.start_time > datetime.now():
            artist = Artist.query.filter(Artist.id==show.artist_id).first()
            upcoming_shows.append({
                'artist_id': artist.id,
                "artist_name": artist.name,
                'artist_image_link': artist.image_link
            })
        else:
            artist = Artist.query.filter(Artist.id==show.artist_id).first()
            past_shows.append({
                'artist_id': artist.id,
                "artist_name": artist.name,
                'artist_image_link': artist.image_link
            })
    return render_template(
        'pages/show_venue.html', 
        venue=venue,
        upcoming_shows=upcoming_shows,
        past_shows = past_shows
    )

@app.route('/venues/create', methods=['GET', 'POST'])
def create_venue():
    if request.method == 'GET':
        form = VenueForm()
        return render_template('forms/new_venue.html', form=form)
    elif request.method == 'POST':
        venue_name = request.form.get('name')
        venue_address = request.form.get('address')
        venue_city = request.form.get('city')
        venue_state = request.form.get('state')
        venue_phone = request.form.get('phone')
        venue_website = request.form.get('website')
        venue_facebook = request.form.get('facebook_link')
        venue_image = request.form.get('image_link')
        venue_talent = str_to_bool(request.form.get('seeking_talent'))
        venue_description = request.form.get('seeking_description')
        try:
            venue = Venue(
                name=venue_name,
                address=venue_address,
                city=venue_city,
                state=venue_state,
                phone=venue_phone,
                # add the genre ids as a relationship to the genres property
                genres=[Genre.query.get(genre_id) for genre_id in request.form.getlist('genres')],
                website=venue_website,
                facebook_link=venue_facebook,
                image_link=venue_image,
                seeking_talent=venue_talent,
                seeking_description=venue_description
            )
            db.session.add(venue)
            db.session.commit()
            flash('Venue ' + venue_name + ' was successfully listed!')
        except Exception as err:
            print(f'Error inserting into venues: {err}')
            flash('An error has occurred inserting your venue')
        finally:
            db.session.close()
        return redirect(url_for('create_venue'))

@app.route('/venues/<int:venue_id>/edit', methods=['GET', 'POST', 'DELETE'])
def render_venue(venue_id):
    # We need to get the venue for any method
    venue = Venue.query.get(venue_id)
    if request.method == 'GET':
        form = VenueForm()
        # recreate the choices so that the chosen is at the top of the list
        form.state.choices=[
            (venue.state, venue.state),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
        venue_genres = [Genre.query.get(genre.id).name for genre in venue.genres]
        return render_template('forms/edit_venue.html', form=form, venue=venue, venue_genres=venue_genres)
    elif request.method == 'POST':
        venue_previous_name = venue.name
        venue_name = request.form.get('name')
        venue_address = request.form.get('address')
        venue_city = request.form.get('city')
        venue_state = request.form.get('state')
        venue_phone = request.form.get('phone')
        venue_website = request.form.get('website')
        venue_facebook = request.form.get('facebook_link')
        venue_image = request.form.get('image_link')
        venue_talent = str_to_bool(request.form.get('seeking_talent'))
        venue_description = request.form.get('seeking_description')
        try:
            venue.name = venue_name
            venue.address = venue_address 
            venue.city = venue_city 
            venue.state = venue_state 
            venue.phone = venue_phone 
            venue.website = venue_website
            venue.facebook_link = venue_facebook
            venue.image_link = venue_image 
            venue.seeking_talent = venue_talent
            venue.seeking_description = venue_description
            db.session.add(venue)
            db.session.commit()
            flash(f'Venue {venue_previous_name} has successfully been editted to {venue_name}')
        except  Exception as err:
            print(f'Error editing venue: {err}')
            flash('An error has occured editing the venue')
        finally:
            db.session.close()
        return redirect(url_for('render_venue', venue_id=venue_id))
        

@app.route('/venues/<int:venue_id>/delete', methods=['Delete'])
def delete_venue(venue_id):
    venue = Venue.query.get(venue_id)
    try:
        db.session.delete(venue)
        db.session.commit()
        flash(f'Venue {venue_name} has successfully been editted')
    except  Exception as err:
        print(f'Error deleting venue: {err}')
        flash('An error has occured deleting the venue')
    finally:
        db.session.close()


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  data = Artist.query.all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
    search_term = request.form.get('search_term')
    artists = Artist.query.with_entities(Artist.id, Artist.name).filter(Artist.name.ilike(f'%{search_term}%')).all()
    data = []
    for artist in artists:
        shows = Show.query.filter(db.and_(Show.artist_id==artist.id, Show.start_time > datetime.now())).count()
        data.append({
            "id": artist.id,
            "name": artist.name,
            "num_upcoming_shows": shows
        })
    response = {
        'count': len(artists),
        'data': data 
    }
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>', methods=['GET'])
def show_artist(artist_id):
    artist = Artist.query.get(artist_id)
    if not artist:
        abort(404)
    shows = Show.query.filter(Show.artist_id==artist.id).all()
    upcoming_shows = []
    past_shows = []
    for show in shows:
        if show.start_time > datetime.now():
            venue = Venue.query.filter(Venue.id==show.venue_id).first()
            upcoming_shows.append({
                'venue_id': venue.id,
                "venue_name": venue.name,
                'venue_image_link': venue.image_link
            })
        else:
            venue = Venue.query.filter(Venue.id==show.venue_id).first()
            past_shows.append({
                'venue_id': venue.id,
                "venue_name": venue.name,
                'venue_image_link': venue.image_link
            })
    return render_template(
        'pages/show_artist.html', 
        artist=artist,
        upcoming_shows=upcoming_shows,
        past_shows=past_shows
    )

@app.route('/artists/<int:artist_id>/edit', methods=['GET', 'POST'])
def render_artist(artist_id):
    artist = Artist.query.get(artist_id)
    if request.method == 'GET':
        form = ArtistForm()
        # recreate the choices so that the chosen is at the top of the list
        form.state.choices=[
            (artist.state, artist.state),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
        artist_genres = [Genre.query.get(genre.id).name for genre in artist.genres]
        return render_template('forms/edit_artist.html', form=form, artist=artist, artist_genres=artist_genres)
    elif request.method == 'POST':
        artist_previous_name = artist.name
        artist_name = request.form.get('name')
        artist_address = request.form.get('address')
        artist_city = request.form.get('city')
        artist_state = request.form.get('state')
        artist_phone = request.form.get('phone')
        artist_website = request.form.get('website')
        artist_facebook = request.form.get('facebook_link')
        artist_image = request.form.get('image_link')
        artist_venue = str_to_bool(request.form.get('seeking_venue'))
        artist_description = request.form.get('seeking_description')
        try:
            artist.name = artist_name
            artist.address = artist_address 
            artist.city = artist_city 
            artist.state = artist_state 
            artist.phone = artist_phone 
            artist.website = artist_website
            artist.facebook_link = artist_facebook
            artist.image_link = artist_image 
            artist.seeking_venue = artist_venue
            artist.seeking_description = artist_description
            db.session.add(artist)
            db.session.commit()
            flash(f'Artist {artist_previous_name} has successfully been editted to {artist_name}')
        except  Exception as err:
            print(f'Error editing artist: {err}')
            flash('An error has occurred editing the artist')
        finally:
            db.session.close()
        return redirect(url_for('render_artist', artist_id=artist_id))

@app.route('/artists/<int:artist_id>/delete', methods=['DELETE'])
def delete_artist(artist_id):
    artist = Artist.query.get(artist_id)
    try:
        db.session.delete(artist)
        db.session.commit()
        flash(f'Artist {artist_name} has successfully been editted')
    except  Exception as err:
        print(f'Error deleting artist: {err}')
        flash('An error has occured deleting the artist')
    finally:
        db.session.close()

@app.route('/artists/create', methods=['GET', 'POST'])
def create_artist():
    if request.method == 'GET':
        form = ArtistForm()
        return render_template('forms/new_artist.html', form=form)
    elif request.method == 'POST':
        artist_name = request.form.get('name')
        artist_address = request.form.get('address')
        artist_city = request.form.get('city')
        artist_state = request.form.get('state')
        artist_phone = request.form.get('phone')
        artist_website = request.form.get('website')
        artist_facebook = request.form.get('facebook_link')
        artist_image = request.form.get('image_link')
        seeking_venue = str_to_bool(request.form.get('seeking_venue'))
        artist_description = request.form.get('seeking_description')
        try:
            artist = Artist(
                name=artist_name,
                city=artist_city,
                state=artist_state,
                phone=artist_phone,
                # add the genre ids as a relationship to the genres property
                genres=[Genre.query.get(genre_id) for genre_id in request.form.getlist('genres')],
                website=artist_website,
                facebook_link=artist_facebook,
                image_link=artist_image,
                seeking_venue=seeking_venue,
                seeking_description=artist_description
            )
            db.session.add(artist)
            db.session.commit()
            flash('Artist ' + artist_name + ' was successfully listed!')
        except Exception as err:
            print(f'Error inserting into artists: {err}')
            flash('An error has occurred inserting your artist')
        finally:
            db.session.close()
        return redirect(url_for('create_artist'))


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    data = []
    shows = Show.query.all()
    for show in shows:
        venue = Venue.query.with_entities(Venue.id, Venue.name).filter(Venue.id==show.venue_id).first()
        artist = Artist.query.with_entities(Artist.id, Artist.name, Artist.image_link).filter(Artist.id==show.artist_id).first()
        data.append({
            'venue_id': venue.id,
            'venue_name': venue.name,
            'artist_id': artist.id,
            'artist_name': artist.name,
            'artist_image_link': artist.image_link,
            'start_time': show.start_time
        })
    return render_template('pages/shows.html', shows=data)

@app.route('/shows/create', methods=['GET', 'POST'])
def create_show():
    if request.method == 'GET':
        form = ShowForm()
        return render_template('forms/new_show.html', form=form)
    elif request.method == 'POST':
        artist_id = request.form.get('artist_id')
        venue_id = request.form.get('venue_id')
        start_time = request.form.get('start_time')
        try:
            show = Show(
                start_time = start_time,
                artist_id=artist_id,
                venue_id=venue_id
            )
            db.session.add(show)
            db.session.commit()
            flash('Show was successfully listed!')
        except Exception as err:
            print(f'An error has occured inserting the show: {err}')
            flash('An error has occured and the show could not be listed')
        finally:
            db.session.close()
        return redirect(url_for('create_show'))

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
