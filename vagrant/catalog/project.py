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
def showArtCatalog():
    # get data
    arts = session.query(Art).all()
    pictures = session.query(Picture).all()

    pictures = getFrontImage(pictures)

    print pictures[0].filename

    return render_template('art.html', arts = arts, pictures = pictures)

@app.route('/art/<int:art_id>/')
@app.route('/art/<int:art_id>/collection:')
def showCollectionItems(art_id):
    return render_template('items.html')


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
