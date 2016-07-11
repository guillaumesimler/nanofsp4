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

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker

# !!!! To be updated  once defined!!!!!
# from database_setup import Base, Restaurant, MenuItem, User 

# 3. oauth2client: Manages the authorization &authentication processes 

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

# 4. Helper modules

import random
import string
import httplib2
import json
import requests


"""
	II. Initizalization
"""

# 1. Define app
app = Flask(__name__)

# 2. Connect to Database and create database session

# engine = create_engine('sqlite:///restaurantmenu.db')
# Base.metadata.bind = engine

# DBSession = sessionmaker(bind=engine)
# session = DBSession()

# 3. Load Client Secret File (Google)

# !!!! To be updated  once defined!!!!!
#CLIENT_ID = json.loads(
#  	open('client_secrets.json', 'r').read())['web']['client_id']


"""
	III. Main program
"""

@app.route('/')
@app.route('/art')
def showArtCatalog():
	return render_template('art.html')

"""
	IV. Webserver
"""
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)
