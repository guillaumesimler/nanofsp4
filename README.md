# Catalog Project

Authors
----
* an [important part of the backbone](https://github.com/udacity/fullstack-nanodegree-vm) was designed by the [udacity team](https://github.com/udacity/fullstack-nanodegree-vm/graphs/contributors) under the lead of [Lorenzo Brown](https://www.linkedin.com/in/lorenzobrown), this covers especially **the vagrant configuration as well as its internal setup**


* the **adaptation of the files** was done by **Guillaume Simler**, a Udacity Frontend Nanodegree graduate and Full Stack Web Developer Student, more information and contact details on my [Github profile](https://github.com/guillaumesimler)
	- the setup of the database

Project description
----

The aim is to design an application with a **CRUD backbone** and **authorization**.

This app depicts my **private art collection**, a project I wanted to implemented long ago.

Ressources
----

The app uses the following ressources:

* **Backbone**
	- [Flask](http://flask.pocoo.org/) handling the templates and most of the methods
	- [SQLalchemy](http://www.sqlalchemy.org/) managing the database
	- [SQLite](https://www.sqlite.org/) the database used there
* **Frontend**



Data structure
----

#### Database


#### Tables


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