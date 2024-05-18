from flask import Flask, render_template, url_for, redirect, request, flash
from sqlalchemy.orm import relationship
from flask_alchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user

#Initiliaze flask app
app = Flask(__name__)

#configure sqlalchemy, flask login
app.config['SECRET_KEY'] = 'MY_KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = ""
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    """Class to store user information"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), unique=False, nullable=False)
    phone_number = db.Column(db.Integer, unique=False, nullable=False)
    agency = db.Column(db.String, unique=False, nullable=False)
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

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'], endpoint='login')
def login():
    """handles login request"""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password. Please try again.')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'], endpoint='register')
def register():
    """handles creating account request"""
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        agency = request.form['agency']
        password = request.form['password']
        if User.query.filter_by(email=email).first():
            flash('There is an account associated with this email.')
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, agency=agency, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('create_account.html')


if __name__ == '__main__':
    app.run(debug=True)
