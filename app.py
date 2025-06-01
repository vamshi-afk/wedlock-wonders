from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from mysql.connector import Error
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Strong random secret key for sessions

# Database connection function
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='username',         # Change to your MySQL username
        password='yourpassword', # Change to your MySQL password
        database='wedlockwonders'
    )
    return connection

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Check if username exists
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('Username already exists.', 'danger')
            cursor.close()
            connection.close()
            return redirect(url_for('register'))
        else:
            # Hash the password before storing
            hashed_password = generate_password_hash(password)
            cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, hashed_password))
            connection.commit()

            cursor.close()
            connection.close()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Fetch user by username only
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        # Verify password hash
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['user_id']
            session['user_name'] = user['username']
            flash('Login successful!', 'success')
            return redirect(url_for('book'))
        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
    
    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    session.clear()  # Clear the session
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))  # Redirect to home page after logging out

# Home route (index)
@app.route('/')
def index():
    if 'user_id' not in session:
        return render_template('index.html')  # Show home page if user is not logged in
    else:
        return render_template('index_logged_in.html')  # Show different page if logged in

# Function to get venue price
def get_venue_price(venue_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT price FROM venues WHERE venue_id = %s', (venue_id,))
    venue = cursor.fetchone()
    connection.close()
    return venue['price'] if venue else 0

# Function to get price for catering, orchestra, or decoration
def get_service_price(service_type, service_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    if service_type == 'catering':
        cursor.execute('SELECT price FROM catering WHERE catering_id = %s', (service_id,))
    elif service_type == 'orchestra':
        cursor.execute('SELECT price FROM orchestra WHERE orchestra_id = %s', (service_id,))
    elif service_type == 'decoration':
        cursor.execute('SELECT price FROM decorations WHERE decoration_id = %s', (service_id,))
    
    service = cursor.fetchone()
    connection.close()
    return service['price'] if service else 0

# Book page route
@app.route('/book', methods=['GET', 'POST'])
def book():
    if 'user_id' not in session:
        flash("You must be logged in to book a venue!", "danger")
        return redirect(url_for('login'))

    if request.method == 'POST':
        venue_id = request.form['venue_id']
        orchestra_option = request.form['orchestra_option']
        decoration_option = request.form['decoration_option']
        catering_option = request.form['catering_option']
        date = request.form['date']
        user_id = session.get('user_id')  # Get logged in user_id

        # Get the prices for each service
        venue_price = get_venue_price(venue_id)
        catering_price = get_service_price('catering', catering_option)
        orchestra_price = get_service_price('orchestra', orchestra_option)
        decoration_price = get_service_price('decoration', decoration_option)

        # Calculate the total price
        total_price = venue_price + catering_price + orchestra_price + decoration_price

        # Insert booking into the bookings table
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO bookings (user_id, venue_id, catering_id, orchestra_id, decoration_id, booking_date, total_price) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (user_id, venue_id, catering_option, orchestra_option, decoration_option, date, total_price))
        connection.commit()

        # Get the booking ID of the just inserted booking
        booking_id = cursor.lastrowid
        cursor.close()
        connection.close()

        flash(f"Your booking has been confirmed! Booking ID: {booking_id}", "success")
        return redirect(url_for('your_bookings'))

    # Fetch data for dropdowns (GET request)
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute('SELECT * FROM venues')
    venues = cursor.fetchall()

    cursor.execute('SELECT * FROM orchestra')
    orchestra_options = cursor.fetchall()

    cursor.execute('SELECT * FROM decorations')
    decoration_options = cursor.fetchall()

    cursor.execute('SELECT * FROM catering')
    catering_options = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('book.html', venues=venues, orchestra_options=orchestra_options, decoration_options=decoration_options, catering_options=catering_options)

# Your bookings page route
@app.route('/your_bookings')
def your_bookings():
    connection = get_db_connection()

    if connection is None:
        flash("Unable to connect to the database. Please try again later.")
        return redirect(url_for('index'))

    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT b.booking_id, v.name AS venue_name, c.name AS catering_name, 
                   o.name AS orchestra_name, d.name AS decoration_name, 
                   b.booking_date, b.total_price
            FROM bookings b
            LEFT JOIN venues v ON b.venue_id = v.venue_id
            LEFT JOIN catering c ON b.catering_id = c.catering_id
            LEFT JOIN orchestra o ON b.orchestra_id = o.orchestra_id
            LEFT JOIN decorations d ON b.decoration_id = d.decoration_id
            WHERE b.user_id = %s
        """, (session['user_id'],))

        bookings = cursor.fetchall()

        if not bookings:
            flash("You have no bookings.")
            return render_template('your_bookings.html', bookings=bookings)

        return render_template('your_bookings.html', bookings=bookings)
    
    except Error as e:
        flash(f"An error occurred while fetching data: {e}")
        return redirect(url_for('index'))
    
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)
