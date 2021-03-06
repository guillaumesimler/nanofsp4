# Catalog Project

Authors
----
* an [important part of the backbone](https://github.com/udacity/fullstack-nanodegree-vm) was designed by the [udacity team](https://github.com/udacity/fullstack-nanodegree-vm/graphs/contributors) under the lead of [Lorenzo Brown](https://www.linkedin.com/in/lorenzobrown), this covers especially
	- **the vagrant configuration as well as its internal setup**
	- the Google Oauth Setup


* the **design of the application** was done by **Guillaume Simler**, a Udacity Frontend Nanodegree graduate and Full Stack Web Developer Student, more information and contact details on my [Github profile](https://github.com/guillaumesimler)
	- the setup of the database
	- the backbone logic in python
	- the front end

Project description
----

The aim is to design an application with a **CRUD backbone** and **authorization**.

This app depicts my **private art collection**, a project I wanted to implemented long ago.


Discussion
----
A lot of the modifications were discussed in [Github](https://github.com/guillaumesimler/nanofsp4/issues?utf8=%E2%9C%93&q=)

#### What should ...

##### ... come in and will be worked on (a separate branch)

* A **second oauth** [(Linkedin?)](https://developer.linkedin.com/docs/oauth2#!)#
* A **local oauth** server
* Getting an picture for the artworks displayed in arts

##### ... come in but requires (your, aka the reviewer's) help

* Getting the files upload for the picture. I tried with
	- a classic form, but failed due to browser security (__\fakepath\__)
	- with blobs, but would need to deepen my reseach (as they disappeared when I loaded the POST request)

##### ... come in, but won't

* a better responsiveness
* modals for the pictures

#### How are thinks JSONified?

The specific JSON accesses don't retrieve **all** data but only the **main** data, e.g. the artwork will
* retrieve the selected artworks
* not the related pictures

Ressources
----

The app uses the following ressources:

* **Backbone**
	- [Flask](http://flask.pocoo.org/) handling the templates and most of the methods
	- [SQLalchemy](http://www.sqlalchemy.org/) managing the database
	- [SQLite](https://www.sqlite.org/) the database used there
	- [oauth2client](https://github.com/google/oauth2client), the library enabling the use of [Oauth2](http://oauth.net/2/)
	- Helper modules, such as [random](https://docs.python.org/2/library/random.html), [string](https://docs.python.org/2/library/string.html), [json](https://docs.python.org/2.7/library/json.html),
	- HTTP helper modules, such as [Requests](http://docs.python-requests.org/en/master/) and [httplib2](https://pypi.python.org/pypi/httplib2)
* **Frontend**
	- [Jquery](https://jquery.com/)
	- [Bootstrap](http://getbootstrap.com/)


How to use
----

#### Initialize the project

* Clone the [Repo](https://github.com/guillaumesimler/nanofsp4)
* Set up your [vagrant machine and make sure to have a virtual machine](https://udacity.atlassian.net/wiki/display/BENDH/Vagrant+VM+Installation)
* Once installed, use your terminal to "cd" to the /vagrant/catalog or git bash window on this folder
* Setup the project database

```shell
	python project_database.py
```

* Populate the database
```shell
	python project_populate.py
```

**The project should be setup**

#### Run the project after Initialization

* Start the webserver

```shell
	python project_database.py
```

* Load the website on the [localhost http://localhost:8000/art](http://localhost:8000/art)
* have fun

Repository
----
* the [working project](https://github.com/guillaumesimler/nanofsp4)

License
----

The **current version** is under [_MIT License_](https://github.com/guillaumesimler/nanofsp4/blob/master/LICENSE.txt)