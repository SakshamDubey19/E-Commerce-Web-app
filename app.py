from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import engine, User, Product, Session

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

@app.route('/category/<string:category>')
def view_category(category):
    if 'user' not in session:
        flash('Please log in to access the dashboard.', 'warning')
        return redirect(url_for('login'))
    
    products = db_session.query(Product).filter_by(category=category).all()
    return render_template('category_products.html', category=category, products=products)

if __name__ == '__main__':
    app.run(debug=True)
