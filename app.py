from flask import Flask, render_template, url_for, redirect, request, flash
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user
import os
from flask_mail import Mail, Message

#Initiliaze flask app
app = Flask(__name__)

#configure sqlalchemy, flask login
app.config['SECRET_KEY'] = 'MY_KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://emogyreunion:mark734@localhost/realestate"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['MAIL_SERVER'] = 'smtp@gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'info.markrealestateapp734@gmail.com'
app.config['MAIL_PASSWORD'] = 'MY_PASSWORD'

mail = Mail(app)
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
    phone_number = db.Column(db.String(50), unique=False, nullable=False)
    agency = db.Column(db.String(50), unique=False, nullable=False)
    properties = relationship('Property', backref='user', lazy=True)


class Property(db.Model):
    """Maps table to store property information"""
    __tablename__ = 'properties'

    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    bedrooms = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    features = db.Column(db.String(250), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    for_rent = db.Column(db.Boolean, nullable=False)
    images = relationship('Image', backref='property', lazy=True, cascade='all, delete-orphan')


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


@app.route('/dashboard', methods=['POST'], endpoint='dashboard')
@login_required
def dashboard():
    """render logged in users dashboard"""
    return render_template('dashboard.html')


@app.route('/upload', methods=['GET', 'POST'], endpoint='upload')
@login_required
def upload():
    if request.method == 'POST':
        location = request.form['location']
        price = float(request.form['price'])
        bedrooms = int(request.form['bedrooms'])
        description = request.form['description']
        features = request.form['features']
        for_rent = request.form['for_rent'].lower() == 'true'
        user_id = current_user.id

        my_property = Property(location=location, price=price, bedrooms=bedrooms, user_id=user_id, for_rent=for_rent)
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

@app.route('/uploads')
@login_required
def uploads():
    """Retrieves property associated with a user"""
    user_id = current_user.id
    properties_with_images = Property.query.filter_by(user_id=user_id).options(db.joinedload('images')).all()
    return render_template('uploads.html', properties_with_images=properties_with_images)

@app.route('/details/<int:property_id>')
@login_required
def details(property_id):
    """Retrieves property details"""
    property_with_images = Property.query.filter_by(id=property_id).options(db.joinedload('images')).first()
    return render_template('details.html', property_with_images=property_with_images)


@app.route('/delete_property/<int:property_id>', methods=['POST'])
@login_required
def delete_property(property_id):
    """Deletes a property based on its property_id"""
    property1 = Property.query.filter_by(id=property_id)
    if property1 and property1.user_id == current_user.id:
        db.session.delete(property1)
        db.session.commit()
        flash('Property deleted successfully.')
    else:
        flash('Property not found or you do not have permission to delete it.')

    return redirect(url_for('uploads'))

@app.route('/update_property/<int:property_id>', methods=['GET', 'PATCH'])
@login_required
def update_property(property_id):
    """Updates property with specific id"""
    property1 = Property.query.get_or_404(property_id)
    
    if property1.user_id != current_user.id:
        flash('Unauthorized access', 'error')
        return redirect(url_for('uploads'))
    
    if request.method == 'GET':
        return render_template('update.html', property1=property1)
    
    if request.method == 'PATCH':
        data = request.form
        
        if not data:
            flash('Bad Request', 'error')
            return redirect(url_for('uploads'))
        
        if 'location' in data:
            property1.location = data['location']
        
        if 'price' in data:
            property1.price = float(data['price'])
        
        if 'bedrooms' in data:
            property1.bedrooms = int(data['bedrooms'])
        
        if 'features' in data:
            property1.features = data['features']
        
        if 'description' in data:
            property1.description = data['description']
        
        if 'for_rent' in data:
            property1.for_rent = data['for_rent'].lower() == 'true'
        
        db.session.commit()
        flash('Updated successfully', 'success')
        return redirect(url_for('uploads'))

@app.route('/send_email/<int:user_id>', methods=['POST'])
def send_email(user_id):
    """Sends an email to a specific user based on form submission."""
    user = User.query.get(user_id)
    if not user:
        return "User not found", 404
    
    data = request.form

    email = data.get('email')
    name = data.get('name')
    message = data.get('message')

    if not all([email, name, message]):
        return "Missing form data", 400

    msg = Message(
        subject='Contact Form Submission',
        sender=('RealEstateApp', 'info.markrealestateapp734@gmail.com'),
        recipients=[user.email]
    )

    msg.body = f"Name: {name}\nEmail: {email}\nMessage: {message}"

    try:
        mail.send(msg)
        return "Email sent successfully", 200
    except Exception as e:
        return str(e), 500


@app.route('/sale')
def get_sale():
    """Retrieves all properties for sale"""
    properties_with_images = Property.query.filter_by(for_rent=False).options(db.joinedload('images')).all()
    return render_template('sale.html', properties_with_images=properties_with_images)


@app.route('/rent')
def get_rent():
    """Retrieves all properties for rent"""
    properties_with_images = Property.query.filter_by(for_rent=True).options(db.joinedload('images')).all()
    return render_template('rent.html', properties_with_images=properties_with_images)


@app.route('/property_details/<int:property_id>')
def property_details(property_id):
    """Retrieves property details"""
    property_with_images = Property.query.filter_by(id=property_id).options(db.joinedload('images')).first()
    if not property_with_images:
        return "Property not found", 404
    return render_template('property_details.html', property_with_images=property_with_images)

if __name__ == '__main__':
    app.run(debug=True)
