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
