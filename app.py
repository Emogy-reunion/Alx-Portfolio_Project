from flask import Flask
from flask_alchemy import SQLAlchemy


#Initiliaze flask app
app = Flask(__name__)

#configure sqlalchemy
app.config['SQLALCHEMY_DATABASE_URI'] = ""
db = SQLAlchemy(app)

class User(db.Model):
    """Class to store user information"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), unique=True, nullable=False)
    phone_number = db.Column(db.Integer, unique=True, nullable=False)
    agency = db.Column(db.String, unique=True, nullable=False)
    properties = relationship('Property', backref='user', lazy=True)


class Property(db.Model):
    """Maps table to store property information"""
    __tablename__ = 'properties'

    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    bedrooms = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    features = db.Column(db.String(250), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    images = relationship('Image', backref='property', lazy=True)


class Image(db.Model):
    """stores property filenames"""
    __tablename__ = "images"
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)

db.create_all()

@app.route('/', endpoint='home')
def index():
    """render home page for the main site"""
    return render_template('index.html')

@app.route('/about', endpoint='about')
def about():
    """renders the about page of the main site"""
    return render_template('about.html')

@app.route('/buy', endpoint='buy')
def buy():
    """renders the buy page of the main site"""
    return render_template('buy.html')

@app.route('/rent', endpoint='rent')
def rent():
    """renders the rent page of the main site"""
    return render_template('rent.html')

@app.route('/contact', endpoint='contact')
def contact():
    """renders the contact page of the main site"""
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)
