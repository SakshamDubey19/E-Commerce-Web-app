from flask import Flask, render_template, request, redirect, url_for, session, flash,abort
from models import engine, User, Product, Session
from sqlalchemy.exc import IntegrityError
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Used for session management

# Create a database session
db_session = Session()

# Dummy user for login
DUMMY_USER = {
    'username': 'admin',
    'password': 'password123'
}

@app.route('/')
def home():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == DUMMY_USER['username'] and password == DUMMY_USER['password']:
            session['user'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))
    
    

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        flash('Please log in to access the dashboard.', 'warning')
        return redirect(url_for('login'))
    
    categories = db_session.query(Product.category).distinct().all()
    return render_template('dashboard.html', categories=categories)



@app.route('/', methods=['GET'])
def index():
    return render_template('add_product.html')

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        new_product = Product(
            id=request.form['product_id'],
            name=request.form['product_name'],
            category=request.form['category'],

        )
        try:
            db_session.add(new_product)
            db_session.commit()
            return redirect(url_for('index'))
        except IntegrityError:
            db_session.rollback()
            return render_template('error.html', error='Product ID already exists'), 400
    elif request.method == 'GET':
        return render_template('add_product.html')
    else:
        abort(405)


@app.route('/users-section', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        new_user = User(
            id=request.form['user_id'],
            Username=request.form['username'],
            password=request.form['password'],

        )
        try:
            db_session.add(new_user)
            db_session.commit()
            return redirect(url_for('index'))
        except IntegrityError:
            db_session.rollback()
            return render_template('error.html', error='User ID already exists'), 400
    elif request.method == 'GET':
        cursor = sqlite3.connect('ecommerce.db').cursor()

        cursor.execute("SELECT * FROM Users")
        rows = cursor.fetchall()
        return render_template('users-section.html', users = rows )

    else:
        abort(405)







@app.route('/category/<string:category>')
def view_category(category):
    if 'user' not in session:
        flash('Please log in to access the dashboard.', 'warning')
        return redirect(url_for('login'))
    
    products = db_session.query(Product).filter_by(category=category).all()
    return render_template('category_products.html', category=category, products=products)


    


db_session.close()

if __name__ == '__main__':
    app.run(debug=True)