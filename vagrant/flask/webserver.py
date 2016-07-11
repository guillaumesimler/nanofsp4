# 1. Import the Modules for the webserver

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import bleach

# 2. Import the Modules for the backbones

from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind =engine)
session = DBSession()

# 3. Define the elements of the webserver

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):

        try:

            # 3.1 Hello page 
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>Hello!"

                output += "<form method='POST' enctype='multipart/form-data' action='/hello'> \
                            <h2>What do you want me to say?</h2>\
                            <input name='message' type='text'>\
                            <input type='submit' Value='Say it'>\
                       </form>" 

                output += "</body></html>"

                self.wfile.write(output)
                print output
                return

            # 3.2 hola page 
            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>&#161 Hola! <br> <a href='/hello'> Back to Hello</a>"

                output += "<form method='POST' enctype='multipart/form-data' action='/hello'> \
                            <h2>What do you want me to say?</h2>\
                            <input name='message' type='text'>\
                            <input type='submit' Value='Say it'>\
                       </form>" 

                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            # 3.3 restaurants page 
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body><h1>Restaurants </h1> <br> <a href='/restaurants/new'><b>Create a New Restaurant</b></a>"

                restaurants = session.query(Restaurant).all()

                for restaurant in restaurants:
                    output += "<div class='restaurant'><p><b>%s</b><br>" %restaurant.name
                    output += "<a href='/restaurant/%s/edit'>Edit</a><br>" %restaurant.id
                    output += "<a href=/restaurant/%s/delete>Delete</a>" %restaurant.id
                    output += "</p></div>"

                output += "</body></html>"
                self.wfile.write(output)

                print self.path
                return

            # 3.4 new restaurants page 
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body><h1>Create a new restaurants </h1> <br> <a href='/restaurants'><b>Back to Restaurant</b></a>"

                
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>"
                
                output += "<input name='newrestaurant' type='text' placeholder='New restaurant&#39;s name'> <br>"
                output += "<input type='submit' value='Create new Restaurant'>"
                output += "</form>"

                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            # 3.5 Edit restaurant page 

            if self.path.endswith("/edit"):

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                path = self.path
                resto_id = int(path.split('/')[-2])

                resto = session.query(Restaurant).filter(Restaurant.id ==resto_id).one()

                output = ""
                output += "<html><body><h1>Edit the restaurant: %s</h1>" % resto.name

                output += "<form method='POST' enctype='multipart/form-data' action='%s'>" %self.path
                output += "<input name='editestaurant' type='text' value='%s'> <br>" %resto.name
                output += "<input type='submit' value='Update the Restaurant'>"
                output += "</form>"

                output += "<p><a href='/restaurants'>Abort and return to main page</a></p>"

                output += "</body></html>"

                self.wfile.write(output)


            # 3.6 Delete restaurant page 

            if self.path.endswith("/delete"):

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                path = self.path
                resto_id = int(path.split('/')[-2])

                resto = session.query(Restaurant).filter(Restaurant.id ==resto_id).one()

                menuItems = session.query(MenuItem).filter(MenuItem.restaurant_id == resto_id).all()


                output = ""
                output += "<html><body><h1>Delete the restaurant: %s</h1>" % resto.name
                output += "<h2>Are you sure? This can't be undone.</h2>"

                if len(menuItems) > 0:
                    output += "<p>The %s menu items related to the restaurant will be deleted as well</p>" % len(menuItems)
                else:
                    output += "<p>Luckilly there are no items yet</p>"

                output += "<form method='POST' enctype='multipart/form-data' action='%s'>" %self.path
                output += "<input type='submit' value='Delete'>"
                output += "</form>"

                output += "<p><a href='/restaurants'>Abort and return to main page</a></p>"

                output += "</body></html>"

                self.wfile.write(output)

        except IOError:
            self.send_error(404, "File Not Found %s" %self.path)




    def do_POST(self):

        try:
            # 1. Hello update
            if self.path.endswith("/hello"):
                self.send_response(301)
                self.end_headers()

                ctype, pdict = cgi.parse_header(self.headers.getheader('Content-type'))

                if ctype =='multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')
                  
               

                output = ""

                output += "<html><body>"

                output += "<h2>Okay, how about this: </h2>"
                output += "<h1> %s </h1>" % messagecontent[0]


                output += "<form method='POST' enctype='multipart/form-data' action='/hello'> \
                                <h2>What do you want me to say?</h2>\
                                <input name='message' type='text'>\
                                <input type='submit' Value='Say it'>\
                           </form>" 

                output += "</body></html>"

                self.wfile.write(output)
                print output

            #2. New Restaurant
            if self.path.endswith("/restaurants/new"):
                print self.headers.getheader('Content-type')

                ctype, pdict = cgi.parse_header(self.headers.getheader('Content-type'))

                if ctype =='multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                
                newresto = escape(fields.get('newrestaurant')[0])

                session.add(Restaurant(name = newresto))
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
            
                self.end_headers()


            #3. Edit value
            if self.path.endswith("/edit"):

                path = self.path
                resto_id = int(path.split('/')[-2])

                ctype, pdict = cgi.parse_header(self.headers.getheader('Content-type'))

                if ctype =='multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                
                editresto = escape(fields.get('editestaurant')[0])

                updateresto = session.query(Restaurant).filter(Restaurant.id == resto_id).one()

                updateresto.name = escape(editresto)

                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
            
                self.end_headers()


            # 4. Delete entry
            if self.path.endswith("/delete"):

                path = self.path
                resto_id = int(path.split('/')[-2])

                menuItems = session.query(MenuItem).filter(MenuItem.restaurant_id == resto_id)
                resto = session.query(Restaurant).filter(Restaurant.id ==resto_id)

                if menuItems:
                    menuItems.delete()
                    print "MenuItem ought to be deleted"
                else: 
                    print "no Menuitmes"

                resto.delete()
                print "Restaurant ought to be deleted"

                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
            
                self.end_headers()


        except IOError:
            self.send_error(501, "Server error %s" %self.path)

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print "Web server running on port %s" %port
        server.serve_forever()

    except KeyboardInterrupt:
        print "^C entered, stopping web server..."
        server.socket.close()
    

def escape(value):
    value = bleach.clean(value)
    value = value.replace("'", "&#39;")
    
    return value



if __name__ == '__main__':
    main()