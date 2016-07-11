from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.bind = engine


DBSession = sessionmaker(bind =engine)
session = DBSession()

# 1. Fill restaurants
restaurants = []
restaurants.append(Restaurant(name = "Pizza Gloria"))
restaurants.append(Restaurant(name = "Oberschaenke"))
restaurants.append(Restaurant(name = "Les trois gros"))
restaurants.append(Restaurant(name = "Drovers' inn"))

for restaurant in restaurants:
	session.add(restaurant)

session.commit()
test = len(session.query(Restaurant).all())

print "Data added: " + str(test) + " restaurants"

# 2. Food Item
foods = []

foods.append(MenuItem(name = 'Quatre fromages', course = 'Main', 
                      description = 'Emental, Gorgonzola, Mozarrella & Special choice', 
                      price='11.30 EUR', 
                      restaurant = restaurants[0]))

foods.append(MenuItem(name = 'Foie gras', course = 'Entry', 
                      description = 'Foie gras de canard fait maison', 
                      price='25.00 EUR', 
                      restaurant = restaurants[2]))

foods.append(MenuItem(name = 'Margarita', course = 'Main', 
                      description = 'Tomato & Mozarrella', 
                      price='8.70 EUR', 
                      restaurant = restaurants[0]))

foods.append(MenuItem(name = 'Turbo ', course = 'Main', 
                      description = 'Nice fish dish', 
                      price='45.00 EUR', 
                      restaurant = restaurants[2]))

foods.append(MenuItem(name = 'Vernisson Burger', course = 'Main', 
                      description = 'The best of the Highlands', 
                      price='12.20 EUR', 
                      restaurant = restaurants[3]))

foods.append(MenuItem(name = 'Suelze', course = 'Entry', 
                      description = 'Typical German dish', 
                      price='6.90 EUR', 
                      restaurant = restaurants[2]))




for food in foods:
	session.add(food)

session.commit()

test = len(session.query(MenuItem).all())
print "Data added: " + str(test) + " menuitems"