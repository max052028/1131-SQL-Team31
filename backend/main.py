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
@app.route("/home", methods=["GET", "POST"])
def home():
    if 'username' not in session:
        return redirect("/") # to login page

    return render_template("home.html")

# Query Page
@app.route("/query", methods=["GET", "POST"])
def query():
    if request.method == "POST":

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # recieve query type
        query_type = request.form.get('query')  # e.g. 'country-query'

        if query_type == "country-query":
            country_1 = request.form.get('country-name') 
            cursor.execute(f"""SELECT t.Confirmed as total_cases 
                           FROM country_wise_latest t 
                           WHERE t.Country_Region = %s;
                           """, ((country_1),))
            result = cursor.fetchone()

            # Close the connection
            cursor.close()
            conn.close()

            # need to handle output, redirect to result page
            flash(f"{country_1}'s total cases: {result}", "success") 
            return redirect("/query")

        if query_type == "continent-query":
            continent_1 = request.form.get('continent-name')
            cursor.execute(f"""SELECT SUM(t.TotalCases) as total_cases 
                           FROM  worldometer_data t 
                           WHERE t.Continent = %s 
                           GROUP BY t.Continent;
                           """, ((continent_1),))
            result = cursor.fetchone()

            # Close the connection
            cursor.close()
            conn.close()

            # need to handle output, redirect to result page
            flash(f"{continent_1}'s total cases: {result}", "success") 
            return redirect("/query")

        if query_type == "world-total-query":
            cursor.execute(f"SELECT SUM(t.TotalCases) as total_cases FROM  worldometer_data t;")
            result = cursor.fetchone()

            # Close the connection
            cursor.close()
            conn.close()

            # need to handle output, redirect to result page
            flash(f"world total cases: {result}", "success") 
            return redirect("/query")

        if query_type == "country-comparison":
            country_2 = request.form.get('country-2') 
            country_3 = request.form.get('country-3') 

        if query_type == "peak-query":
            country_4 = request.form.get('country-4') 
            start_date = request.form.get('start-date')
            end_date = request.form.get('end-date')

            cursor.execute(f"""
                           SELECT t.Date, t.New_cases 
                           FROM full_grouped t 
                           WHERE t.Country_Region = '{country_4}' 
                           AND t.Date >= '{start_date}' AND t.Date <= '{end_date}' 
                           AND t.New_cases >= ( SELECT MAX(t1.New_cases) 
                                                FROM full_grouped t1 
                                                WHERE t1.Date >= '{start_date}' AND t1.Date <= '{end_date}' 
                                                AND t1.Country_Region = '{country_4}');
                            """)
            result = cursor.fetchall()

            # Close the connection
            cursor.close()
            conn.close()

            # need to handle output, redirect to result page
            return redirect("/query")

        if query_type == "sum-query":
            country_5 = request.form.get('country-5') 
            start_date = request.form.get('start-date')
            end_date = request.form.get('end-date')

    return render_template("query.html")

# Update Page
@app.route("/update", methods=["GET", "POST"])
def update():
    return render_template("update.html")

# Create_Update Page
@app.route("/create_update", methods=["GET", "POST"])
def create_update():
    if request.method == "POST":

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        country = request.form.get('country')
        date = request.form.get('date')
        new_cases = request.form.get('cases')

        cursor.execute(f"""""")

    return render_template("create_update.html")

# Delete Page
@app.route("/delete", methods=["GET", "POST"])
def delete():
    return render_template("delete.html")

# Logout
@app.route("/logout", methods=["GET"])
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
