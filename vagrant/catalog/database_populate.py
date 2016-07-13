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
print
print "Starting Database population..."
print

# 1. Initial User

user = {"name" : "admin", "email" : "admin@myartcatalog.com"}


check_user = session.query(User).filter_by(name = user['name']).all()

if check_user: 
    print "The user %s is already in the database." % user['name']
    print "Please check your input and use the front end" 
else:
    
    insert_user = User(name= escape(user['name']), email= escape(user['email']))
    session.add(insert_user)
    print "The user %s will be added to the database" %user['name']

# 2. Art

arts = [{'type': 'Bronze', 
        'description': 'A classic material used by mankind since the age of the same name. This is by far the most popular cast metal sculpture types'},
        {'type': 'Painting',
         'description': 'The classic collection piece: painting is the application  of paint, pigments on a surface. This has been the major discipline in arts'}]


for art in arts:

    check_art = session.query(Art).filter_by(type = art['type']).all()

    if check_art: 
        print "The art (discipline) %s is already in the database." % art['type']
        print "Please check your input and use the front end" 
    else:
        insert_art = Art(type = escape(art['type']), description= escape(art['description']))
        session.add(insert_art)
        print "The art (discipline) %s will be added to the database" %art['type']


# 3. Artist

artists = [{'name'         : 'Elke Zimmermann',
            'information'  : 'Elke is German contemporary sculptor, living and working in Moersach. I discovered her at an exhibition at Schillingfuerst in 2011. Elke mostly but not exclusivelly creates animal sculptures. Her husband, Reinhard, is a painter of his own right.',
            'url'          : 'http://www.atelier-zimmermann.de/',
            'user_id'      : 1},

           {'name'         : 'Hendrick Bobock',
            'information'  : "Hendrick Bobock is a German painter who had quite an active presence on ebay in the early 2000's before being 'washed out' by Chinese painters. His expressive paintings were at a very interesting price which made them suitable for temporary presentation. Yet a decade later, they weren't the ones sorted out.",
            'url'          : 'https://www.xing.com/profile/Hendrik_Bobock',
            'user_id'      : 1},

           {'name'         : 'Python',
            'information'  : "Python was quite the start in Nantes' epicier des arts, a non-profit and often bankrupt gallery. Pyhton was an art student at the academy. Unfortunately he suffered from psychotic breaks: either he was seddated and could not paint or was off the meds, could paint but was a danger to himself and others. His pictures reflect his medical condition as well as the influence of his studies at that time (e.g. Egon Schiele)",
            'url'          : '',
            'user_id'      : 1},

           {'name'         : 'Alexandre Ouline',
            'information'  : "The Belgian sculptor (1918-1940) worked in the classic Art Deco period, the second important period of modern bronze cast scultpures.",
            'url'          : '',
            'user_id'      : 1},
            ]

for artist in artists:

    check_artist = session.query(Artist).filter_by(name = artist['name']).first()

    if check_artist: 
        print "This artist %s seems to be already in the database." % artist['name']
        print "Please check your input and use the front end" 
    else:
        insert_artist= Artist(name = escape(artist['name']), 
                             information= escape(artist['information']),
                             url = escape(artist['url']),
                             user_id = artist['user_id']
                             )
        session.add(insert_artist)
        print "The artist %s will be added to the database" % artist['name']

print "Committing..."
session.commit()
print "Imports committed"
print

