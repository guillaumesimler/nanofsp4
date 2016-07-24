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
#CLIENT_ID = json.loads(
#   open('client_secrets.json', 'r').read())['web']['client_id']


"""
    III. Main program
"""

@app.route('/')
@app.route('/art')

# Display/read elements
def showArtCatalog():
    # get data
    arts = session.query(Art).all()
    pictures = session.query(Picture).all()
    pictures = getFrontImage(pictures)

    artists = session.query(Artist).all() 

    return render_template('art.html', arts = arts, pictures = pictures, artists = artists)

@app.route('/art/<int:art_id>/')
def showCollectionItems(art_id):
    arts = session.query(Art).all()
    artworks = session.query(Artwork).filter_by(art_id = art_id).all()
    return render_template('items.html', arts = arts, id = art_id, artworks = artworks)


@app.route('/art/artist/<int:artist_id>/')
def showArtists(artist_id):
    artists = session.query(Artist).all()

    return render_template('artists.html', artists = artists, artist_id = artist_id)

@app.route('/art/artworks/<int:artwork_id>')
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

        return redirect(url_for('showCollectionItems', art_id = art_id))
    else:      
        return render_template('art_edit.html', art = art)

@app.route('/art/artworks/<int:artwork_id>/edit/', methods=['GET', 'POST'])
def editArtwork(artwork_id):
    artwork = session.query(Artwork).filter_by(id = artwork_id).one()

    if request.method == 'POST':
        artwork.name = request.form['name']
        print "1"
        artwork.description = request.form['description']
        print "2"
        artwork.purchase_year = request.form['purchase_year']
        print "3"
        artwork.size = request.form['size']
        print "4"
        artwork.weight = request.form['weight']
        print "5"
        artwork.purchase_prize = request.form['purchase_prize']
        print "6"
        artwork.art_id = request.form['art_id']
        print "7"
        artwork.artist_id = request.form['artist_id']

        session.commit
        print "The artwort, %s, was updated" %artwork.name
        return redirect(url_for('showArtworks', artwork_id = artwork_id))
    else:
        arts = session.query(Art).all()
        artists = session.query(Artist).all()
        return render_template('artwork_edit.html', artwork = artwork, arts = arts, artists = artists)
    


"""
    IV. Helper functions
"""

def getFrontImage(list):
    """
        Returns two random pictures from a list
    """
    n = len(list) - 1

    r1 = random.randint(0, n)

    # Make sur the second r2
    r2 = r1
    while r2 == r1 and n > 0:
        r2 = random.randint(0, n)

    return [list[r1], list[r2]]

"""
    V. Webserver
"""
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)
