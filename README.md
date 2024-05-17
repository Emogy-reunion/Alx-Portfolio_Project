# Real Estate Listing App

## App initialization
* I initialized the flask app by import Flask from flask

## Database Initialization
* To initialize my database, I imported SQLAlchemy from flask_alchemy
* SQLAlchemy will be used to map the classes to tables
* I declared three models User, Property, Image
* User stores user information such as users  first name, last name, email, password, properties associated with the user
* properties is a relationship attribute that establishes a one to many relationship with the Property table
* This means one user can be associated with multiple images
* Property class stores property details such as its location, price, bedrooms, images, features etc
* images attribute stores property images
* It establishes a one to many relationship with the Image class meaning one property can have multiple images
* Image class stores the file names of images associated with a property

## Rendering main site pages
* My app is divided into two, it has a logged out experience and logged in experience
* When a user isn't logged in they access a page with a navbar with the following links:  home, about, buy, rent, login andcontact
* When a user clicks home the route ('/') is triggered thus rendering index.html which is logged out experience home page
* When a user clicks about the route ('/about') is initiated thus rendering the about page which is about.html
* When a user clicks buy, the buy page buy.html is rendered by the ('/buy') route
* When a user clicks rent,the rent page which is rent.html is rendered by ('/rent')
* when a User clicks contact, the contact page is rendered by contact.html rendered by ('/contact')
