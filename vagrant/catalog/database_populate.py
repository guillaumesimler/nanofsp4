"""
    Database_populate.py

    * programmed by Guillaume Simler
    * populate the database with a potential backbone 


"""

"""
    I. Import & Initialization
"""

# 1. Import modules

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Art, Artist, Artwork, Picture, User 
from security import escape

# 2. Connect to Database and create database session

engine = create_engine('sqlite:///artcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

"""
    II. Database population
"""

# 1. Initial User

user = {"name" : "admin", "email" : "admin@myartcatalog.com"}


check_user = session.query(User).filter_by(name = user['name']).all()

if check_user: 
    print "The user %s is already in the database." % user['name']
    print "Please check your input and use the front end" 
else:
    
    inser_user = User(name= escape(user['name']), email= escape(user['email']))
    session.add(inser_user)
    print "The user %s will be added to the database" %user['name']


print "Committing..."
session.commit()
print "Imports committed"
