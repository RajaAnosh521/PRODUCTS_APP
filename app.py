from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(500), nullable=False)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        # Check if the email is already in use
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already in use. Please log in.")
            return redirect(url_for("login"))
        
        # Create a new user and add it to the database
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        flash("Account created successfully! Please log in.")
        return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        # Check if user exists in the database
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            return redirect(url_for("dashboard"))
        else:
            flash("Account not found. Please sign up.")
            return redirect(url_for("signup"))
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    products = Product.query.all()
    return render_template("dashboard.html", products=products)

@app.route("/product/create", methods=["GET", "POST"])
def create_product():
    if request.method == "POST":
        image = request.form.get("image")
        name = request.form.get("name")
        description = request.form.get("description")
        
        new_product = Product(image=image, name=name, description=description)
        db.session.add(new_product)
        db.session.commit()
        
        return redirect(url_for("dashboard"))
    return render_template("create_product.html")

@app.route("/product/update/<int:id>", methods=["GET", "POST"])
def update_product(id):
    product = Product.query.get_or_404(id)
    if request.method == "POST":
        product.image = request.form.get("image")
        product.name = request.form.get("name")
        product.description = request.form.get("description")

        db.session.commit()
        return redirect(url_for("dashboard"))
    return render_template("update_product.html", product=product)

@app.route("/product/delete/<int:id>", methods=["POST"])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create database tables if they don't exist
    app.run(debug=True)
