from flask import Flask, url_for, render_template, request, redirect, flash, session
import mysql.connector
import hashlib

# Flask App Initialization
app = Flask(__name__)
app.secret_key = "your_secret_key"

# Database Configuration
db_config = {
    'host': 'localhost',  # MySQL host
    'user': 'root',  # MySQL username
    'password': 'Hsg7gs$#GdA0',  # MySQL password
    'database': 'final_test'  # MySQL database name
}

# Database Connection
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Login Page
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        # Hash the password using SHA-256
        password = hashlib.sha256(password.encode()).hexdigest()

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the user exists in the database and whether the password is correct
        # Query to check the user
        cursor.execute(f"SELECT password FROM users WHERE username = %s", ((username),))
        result = cursor.fetchone() # fetchone() returns None if no record is found

        # Close the connection
        cursor.close()
        conn.close()

        # if user does not exists, back to login page
        if result is None:
            flash(f"Error: user does not exist, please sign up.", "danger")
            return redirect("/")
        # if password not correct, back to login page
        # use index to specify a data, or else != is always the case when comparing two different data types
        if result[0] != password: 
            flash(f"Error: wrong password.", "danger")
            return redirect("/")
        # if pass the check, redirect to the welcome page and store the username in the session
        session['username'] = username
        return redirect("/home")
        
    return render_template("login.html")

# Home Page
@app.route("/home")
def home():
    if 'username' not in session:
        return redirect("/") # to login page
    return render_template("home.html")

# Query Page
@app.route("/query")
def query():
    return render_template("query.html")

# Logout
@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect("/")

# Signup
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        # Hash the password using SHA-256
        password = hashlib.sha256(password.encode()).hexdigest()

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()



        # Add the query to insert a new user into the database
        try:
            # Insert new user into the database
            cursor.execute(f"INSERT INTO users(username, password) VALUES(%s, %s);", ((username, password)))
            conn.commit()
            flash("Account created successfully! Please log in.", "success")
            return redirect("/")
        # if any errors occur in "try" block, show an error message from backend of database (e.g. attempting to insert duplicate primary keys)
        except mysql.connector.Error as err:
            flash(f"Error: {err}", "danger")
        finally:
            cursor.close()
            conn.close()
    
    return render_template("signup.html")


if __name__ == "__main__":
    app.run(debug=True)
