from flask import Flask, render_template, url_for, redirect, request, flash
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user
import os

#Initiliaze flask app
app = Flask(__name__)

#configure sqlalchemy, flask login
app.config['SECRET_KEY'] = 'MY_KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://emogyreunion:mark734@localhost/realestate"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

class User(UserMixin, db.Model):
    """Class to store user information"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), unique=False, nullable=False)
    phone_number = db.Column(db.Integer, unique=False, nullable=False)
    agency = db.Column(db.String(50), unique=False, nullable=False)
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

with app.app_context():
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

@login_required
@app.route('/dashboard', methods=['POST'], endpoint='dashboard')
def dashboard():
    """render logged in users dashboard"""
    return render_template('dashboard.html')

@login_required
@app.route('/upload', methods=['GET', 'POST'], endpoint='upload')
def upload():
    if request.method == 'POST':
        location = request.form['location']
        price = request.form['price']
        bedrooms = request.form['bedrooms']
        description = request.form['description']
        features = request.form['features']
        user_id = current_user.id

        my_property = Property(location=location, price=price, bedrooms=bedrooms, user_id=user_id)
        db.session.add(my_property)
        db.session.commit()

        if 'image[]' not in request.files:
            flash('No file part')
            return redirect(request.url)

        images = request.files.getlist('image[]')
        if not images:
            flash('No selected files')
            return redirect(request.url)

        saved_files = []
        for image in images:
            if image.filename == '':
                flash('No selected file')
                return redirect(request.url)

            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                new_image = Image(filename=filename, property_id=my_property.id)
                db.session.add(new_image)
                saved_files.append(filename)

        if not saved_files:
            flash('No files saved')
            return redirect(request.url)
        else:
            flash('Files saved successfully!')
            return redirect(url_for('uploads'))

    return render_template('upload.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS





if __name__ == '__main__':
    app.run(debug=True)
