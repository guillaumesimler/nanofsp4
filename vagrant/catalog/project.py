""" 
    Project.py

    * Programmed by Guillaume Simler
    * Main program of this application: 
        - the web server is set up
        - the methods (GET/POST) are defined

    More information in the comments and/or README File
"""

"""
    I. Module imports
"""

# 1. Flask: manages the templates

from flask import Flask, render_template, request, redirect, jsonify
from flask import url_for, flash, make_response
from flask import session as login_session

# 2. SQL Alchemy: manages the database

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Art, Artist, Artwork, Picture, User 

# 3. oauth2client: Manages the authorization &authentication processes 

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

# 4. Helper modules

import random
import string
import httplib2
import json
import requests

# 5. Security

from security import escape

"""
    II. Initizalization
"""

# 1. Define app
app = Flask(__name__)

# 2. Connect to Database and create database session

engine = create_engine('sqlite:///artcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# 3. Load Client Secret File (Google)

# !!!! To be updated  once defined!!!!!
#   CLIENT_ID = json.loads(
#   open('client_secrets.json', 'r').read())['web']['client_id']


"""
    III. Main program
"""

@app.route('/')
@app.route('/catalog/')
# Display/read elements
def showArtCatalog():
    # get data
    arts = session.query(Art).all()
    pictures = session.query(Picture).all()
    pictures = getFrontImage(pictures)
    artists = session.query(Artist).all() 

    return render_template('catalog.html', arts = arts, pictures = pictures, artists = artists)


@app.route('/art/<int:art_id>/')
def showArts(art_id):
    arts = session.query(Art).all()
    artworks = session.query(Artwork).filter_by(art_id = art_id).all()
    return render_template('arts.html', arts = arts, id = art_id, artworks = artworks)


@app.route('/artist/<int:artist_id>/')
def showArtists(artist_id):
    artists = session.query(Artist).all()

    return render_template('artists.html', artists = artists, artist_id = artist_id)


@app.route('/artworks/<int:artwork_id>')
def showArtworks(artwork_id):
    artwork = session.query(Artwork).filter_by(id = artwork_id).one()
    pictures = session.query(Picture).filter_by(artwork_id = artwork_id).all()
 
    return render_template('artworks.html', artwork = artwork, pictures = pictures, artwork_id = artwork_id)

# Edit/Update elements

@app.route('/art/<int:art_id>/edit/', methods=['GET', 'POST'])
def editArt(art_id):
    art = session.query(Art).filter_by(id = art_id).one()

    if request.method == 'POST':
        edited_type = request.form['type']
        edited_description = request.form['description']

        art.type = edited_type
        art.description = edited_description

        session.commit()
        print "Entry about %s was updated" %art.type

        return redirect(url_for('showArts', art_id = art_id))
    else:      
        return render_template('art_edit.html', art = art)


@app.route('/artworks/<int:artwork_id>/edit/', methods=['GET', 'POST'])
def editArtwork(artwork_id):
    artwork = session.query(Artwork).filter_by(id = artwork_id).one()

    if request.method == 'POST':

        # Enable the input of a new ART Discipline
        if request.form['new_art'] == 'False':
            artwork.art_id = request.form['art_id']
        else:
            new_value = request.form['add_art']

            # Create the new art entry
            new_Art = Art(type = new_value, user_id= 1 )
            session.add(new_Art)
            session.commit()

            print "A new art type was created"

            # Get the new art id

            new_art = session.query(Art).filter_by(type = new_value).one()
            artwork.art_id = new_art.id

        # Enable the input of a new ARTIST
        if request.form['new_artist'] == 'False':
            artwork.artist_id = request.form['artist_id']
        else:
            new_value = request.form['add_artist']

            # Create the new art entry
            new_Artist = Artist(name = new_value, user_id= 1 )
            session.add(new_Artist)
            session.commit()

            print "A new artist was created"

            # Get the new art id

            new_artist = session.query(Artist).filter_by(name = new_value).one()
            artwork.art_id = new_artist.id

        artwork.name = request.form['name']
        artwork.description = request.form['description']
        artwork.purchase_year = request.form['purchase_year']
        artwork.size = request.form['size']
        artwork.weight = request.form['weight']
        artwork.purchase_prize = request.form['purchase_prize']

        session.commit()

        print "The artwort, %s, was updated" %artwork.name
        return redirect(url_for('showArtworks', artwork_id = artwork_id))

    else:
        arts = session.query(Art).all()
        artists = session.query(Artist).all()

        return render_template('artwork_edit.html', artwork = artwork, arts = arts, artists = artists)


@app.route('/artists/<int:artist_id>/edit/', methods=['GET', 'POST'])
def editArtist(artist_id):
    artist = session.query(Artist).filter_by(id = artist_id).one()

    if request.method == 'POST':
        artist.name = request.form['name']
        artist.information = request.form['information']
        artist.url = request.form['url']

        session.commit()

        print "The artist, %s, was updated" %artist.name

        return redirect(url_for('showArtists', artist_id = artist_id))
    else: 
        return render_template('artist_edit.html', artist = artist)


# New Entry

@app.route('/art/new/', methods=['GET', 'POST'])
def addArt():
    # Placeholder for the user
    user = 1

    if request.method == 'POST':
        new_type = request.form['type']
        new_description = request.form['description']

        new_Art = Art(type = new_type, 
                      description = new_description, 
                      user_id = user)

        session.add(new_Art)
        session.commit()

        print "Entry about %s was created" %new_type
        
        new_id = session.query(Art).filter_by(type = new_type).one()

        return redirect(url_for('showArts', art_id = new_id.id))
    else:      
        return render_template('art_add.html')


@app.route('/artworks/new/', methods=['GET', 'POST'])
def addArtwork():

    if request.method == 'POST':
        user = 1
        # Enable the input of a new ART Discipline
        if request.form['new_art'] == 'False':
            new_art_id = request.form['art_id']
        else:
            new_value = request.form['add_art']

            # Create the new art entry
            new_Art = Art(type = new_value, user_id = user)
            session.add(new_Art)
            session.commit()

            print "A new art type was created"

            # Get the new art id

            new_art = session.query(Art).filter_by(type = new_value).one()
            new_art_id = new_art.id

        # Enable the input of a new ARTIST
        if request.form['new_artist'] == 'False':
            new_artist_id = request.form['artist_id']
        else:
            new_value = request.form['add_artist']

            # Create the new art entry
            new_Artist = Artist(name = new_value, user_id = user)
            session.add(new_Artist)
            session.commit()

            print "A new artist was created"

            # Get the new art id

            new_artist = session.query(Artist).filter_by(name = new_value).one()
            new_artist_id  = new_artist.id

        # Get the other input fields
        new_name = request.form['name']
        new_description = request.form['description']
        new_purchase_year = request.form['purchase_year']
        new_size = request.form['size']
        new_weight = request.form['weight']
        new_purchase_prize = request.form['purchase_prize']

        # Create the new entry
        new_artwork = Artwork(name = new_name,
                              description = new_description, 
                              purchase_year = new_purchase_year,
                              size = new_size,
                              weight = new_weight,
                              purchase_prize = new_purchase_prize,
                              user_id = user,
                              art_id = new_art_id,
                              artist_id = new_artist_id)
        session.add(new_artwork)
        session.commit()

        # Get the new id

        new_artwork_id = session.query(Artwork).filter_by(name = new_name).one()

        print "The artwort, %s, was updated" %new_name
        return redirect(url_for('showArtworks', artwork_id = new_artwork_id.id))

    else:
        arts = session.query(Art).all()
        artists = session.query(Artist).all()

        return render_template('artwork_edit.html', arts = arts, artists = artists)


# Delete Entry

@app.route('/art/<int:art_id>/delete/', methods=['GET', 'POST'])
def deleteArt(art_id):
    art = session.query(Art).filter_by(id = art_id).one()
    artworks = session.query(Artwork).filter_by(art_id = art_id).all()
    nb = len(artworks)

    if request.method == 'POST':

        for artwork in artworks:
            session.delete(artwork)
            
        session.delete(art)
        session.commit()
        print "Entry and artworks related to %s were delete" %art.type
        return redirect(url_for('showArtCatalog'))
    else: 
        return render_template('art_delete.html', art = art, artworks = artworks, nb = nb)


@app.route('/artworks/<int:artwork_id>/delete/', methods=['GET', 'POST'])
def deleteArtwork(artwork_id):
    artwork = session.query(Artwork).filter_by(id = artwork_id).one()
    pictures = session.query(Picture).filter_by(artwork_id = artwork_id).all()

    nb = len(pictures)

    if request.method == 'POST':

        for picture in pictures:
            session.delete(picture)
            
        session.delete(artwork)
        session.commit()
        print "Entry and pictures related to %s were delete" %artwork.name
        return redirect(url_for('showArtCatalog'))
    else: 
        return render_template('artwork_delete.html', artwork = artwork, nb = nb)


@app.route('/artists/<int:artist_id>/delete/', methods=['GET', 'POST'])
def deleteArtist(artist_id):
    artist = session.query(Artist).filter_by(id = artist_id).one() 
    artworks = session.query(Artwork).filter_by(artist_id = artist_id).all()
    nb = len(artworks)

    if request.method == 'POST':

        for artwork in artworks:
            session.delete(artwork)
            
        session.delete(artist)
        session.commit()
        print "Entry and artworks related to %s were delete" %artist.name
        return redirect(url_for('showArtCatalog'))
    else: 
        return render_template('artist_delete.html', artist = artist, artworks = artworks, nb = nb)

"""
    IV. Helper functions
"""

def getFrontImage(list):
    """
        Returns two random pictures from a list
    """
    n = len(list) - 1

    # Get number of the Elements
    nb = session.query(Art).all()
    nb = len(nb)

    result = []

    r1 = random.randint(0, n)

    result.append(list[r1])

    # Make sur the second r2
    for x in xrange(1, nb):
        r2 = r1
        while r2 == r1 and n > 0:
            r2 = random.randint(0, n)

        result.append(list[r2])

    return result

"""
    V. Webserver
"""
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)
