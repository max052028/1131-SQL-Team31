from flask import Flask, url_for, render_template, request, redirect, flash, session
from datetime import datetime
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

def execute_query(query, params=None, fetch="all"):
    print("Executing query:", query) # debug
    print("With params:", params) # debug

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        if fetch == "one":
            result = cursor.fetchone()
        else:
            result = cursor.fetchall()

        print("Query result:", result) # debug
        conn.commit()
        return result
    except Exception as err:
        print(f"Database error: {err}")
        return None
    finally:
        cursor.close()
        conn.close()

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
    # extract result from query
    extracted_result = session.get('result_data', None)
    # print("Session result data:", extracted_result) # debug
    session.pop('result_data', None) 


    if request.method == "POST":
        # print("POST request received.") # debug

        # recieve query type
        query_type = request.form.get('query')  # e.g. 'country-query'
        result = None

        # print("Query type received:", query_type)  # debug

        if query_type == "country-total-query":
            country = request.form.get('country-1') 
            print("request.form.get: ", country) # debug
            result = execute_query(f""" SELECT t.Confirmed as total_cases 
                                        FROM country_wise_latest t 
                                        WHERE t.Country_Region = %s;
                                        """, (country,), fetch="one")
            
            result_2 = execute_query(f""" SELECT t.Deaths as total_cases 
                                        FROM country_wise_latest t 
                                        WHERE t.Country_Region = %s;
                                        """, (country,), fetch="one")
            result_3 = execute_query(f""" SELECT t.Recovered as total_cases 
                                        FROM country_wise_latest t 
                                        WHERE t.Country_Region = %s;
                                        """, (country,), fetch="one")
            # show results
            flash(f"""{country}'s 
                  <br>total cases: {result[0]} 
                  <br>total deaths: {result_2[0]} 
                  <br>total recovered: {result_3[0]}""", "success")


        elif query_type == "continent-total-query":
            continent = request.form.get('continent-1')
            result = execute_query(f""" SELECT SUM(t.TotalCases) as total_cases 
                                        FROM  worldometer_data t 
                                        WHERE t.Continent = %s;
                                        """, (continent,), fetch="one")
            
            result_2 = execute_query(f""" SELECT SUM(t.TotalDeaths) as total_cases 
                                        FROM  worldometer_data t 
                                        WHERE t.Continent = %s;
                                        """, (continent,), fetch="one")
            
            result_3 = execute_query(f""" SELECT SUM(t.TotalRecovered) as total_cases 
                                        FROM  worldometer_data t 
                                        WHERE t.Continent = %s;
                                        """, (continent,), fetch="one")
            # show results
            flash(f"""{continent}'s 
                    <br>total cases: {result[0]}
                    <br>total deaths: {result_2[0]}
                    <br>total recovered: {result_3[0]}
                    """, "success")


        elif query_type == "world-total-query":
            result = execute_query(f""" SELECT SUM(t.TotalCases) as total_cases 
                                        FROM  worldometer_data t;""", (), fetch="one")

            result_2 = execute_query(f""" SELECT SUM(t.TotalDeaths) as total_cases 
                                        FROM  worldometer_data t;""", (), fetch="one")
            
            result_3 = execute_query(f""" SELECT SUM(t.TotalRecovered) as total_cases 
                                        FROM  worldometer_data t;""", (), fetch="one")
            # show results
            flash(f"""world's total cases: {result[0]}
                    <br>world's total deaths: {result_2[0]}
                    <br>world's total recovered: {result_3[0]}
                    """, "success")


        elif query_type == "country-peak-query":
            country = request.form.get('country-4') 
            start_date = request.form.get('start-date1')
            end_date = request.form.get('end-date1')

            result = execute_query(f"""
                                    SELECT t.Date, t.New_cases 
                                    FROM full_grouped t 
                                    WHERE t.Country_Region = %s 
                                    AND t.Date >= %s AND t.Date <= %s 
                                    AND t.New_cases >= 
                                    ( 
                                    SELECT MAX(t1.New_cases) 
                                    FROM full_grouped t1 
                                    WHERE t1.Date >= %s 
                                    AND t1.Date <= %s 
                                    AND t1.Country_Region = %s
                                    );
                            """, (country, start_date, end_date, start_date, end_date, country), fetch="all")
            
            result_2 = execute_query(f"""
                                    SELECT t.Date, t.New_deaths 
                                    FROM full_grouped t 
                                    WHERE t.Country_Region = %s 
                                    AND t.Date >= %s AND t.Date <= %s 
                                    AND t.New_deaths >= 
                                    ( 
                                    SELECT MAX(t1.New_deaths) 
                                    FROM full_grouped t1 
                                    WHERE t1.Date >= %s 
                                    AND t1.Date <= %s 
                                    AND t1.Country_Region = %s
                                    );
                            """, (country, start_date, end_date, start_date, end_date, country), fetch="all")
            
            result_3 = execute_query(f"""
                                    SELECT t.Date, t.New_recovered 
                                    FROM full_grouped t 
                                    WHERE t.Country_Region = %s 
                                    AND t.Date >= %s AND t.Date <= %s 
                                    AND t.New_recovered >= 
                                    ( 
                                    SELECT MAX(t1.New_recovered) 
                                    FROM full_grouped t1 
                                    WHERE t1.Date >= %s 
                                    AND t1.Date <= %s 
                                    AND t1.Country_Region = %s
                                    );
                            """, (country, start_date, end_date, start_date, end_date, country), fetch="all")
            
            # show results
            flash(f"""{country}'s between {start_date} and {end_date} has: 
                  <br>peak in cases at {result[0][0]}, where there were {int(result[0][1])} new cases
                  <br>peak in deaths at {result_2[0][0]}, where there were {int(result_2[0][1])} new deaths
                  <br>peak in recovered at {result_3[0][0]}, where there were {int(result_3[0][1])} new recovered""", "success")


        elif query_type == "continent-peak-query":
            continent = request.form.get('continent-2') 
            start_date = request.form.get('continent-peak-start-date')
            end_date = request.form.get('continent-peak-end-date')
            print("Form data received:", request.form) # debug

            result = execute_query(f"""
                                    SELECT t2.Date, SUM(t2.New_cases) AS sum_cases 
                                    FROM worldometer_data t1 
                                    INNER JOIN full_grouped t2 
                                    ON t1.Country_Region = t2.Country_Region 
                                    WHERE t1.Continent = %s 
                                    AND t2.Date >= %s 
                                    AND t2.Date <= %s 
                                    GROUP BY t2.Date 
                                    HAVING SUM(t2.New_cases) = 
                                    ( 
                                    SELECT MAX(sub_query.daily_sum) 
                                    FROM 
                                    ( 
                                    SELECT t2.Date, SUM(t2.New_cases) AS daily_sum 
                                    FROM worldometer_data t1 
                                    INNER JOIN full_grouped t2 
                                    ON t1.Country_Region = t2.Country_Region 
                                    WHERE t1.Continent = %s 
                                    AND t2.Date >= %s 
                                    AND t2.Date <= %s 
                                    GROUP BY t2.Date 
                                    ) AS sub_query 
                                    );    
                            """, (continent, start_date, end_date, continent, start_date, end_date), fetch="one")

            result_2 = execute_query(f"""
                                    SELECT t2.Date, SUM(t2.New_deaths) AS sum_cases 
                                    FROM worldometer_data t1 
                                    INNER JOIN full_grouped t2 
                                    ON t1.Country_Region = t2.Country_Region 
                                    WHERE t1.Continent = %s 
                                    AND t2.Date >= %s 
                                    AND t2.Date <= %s 
                                    GROUP BY t2.Date 
                                    HAVING SUM(t2.New_deaths) = 
                                    ( 
                                    SELECT MAX(sub_query.daily_sum) 
                                    FROM 
                                    ( 
                                    SELECT t2.Date, SUM(t2.New_deaths) AS daily_sum 
                                    FROM worldometer_data t1 
                                    INNER JOIN full_grouped t2 
                                    ON t1.Country_Region = t2.Country_Region 
                                    WHERE t1.Continent = %s 
                                    AND t2.Date >= %s 
                                    AND t2.Date <= %s 
                                    GROUP BY t2.Date 
                                    ) AS sub_query 
                                    );    
                            """, (continent, start_date, end_date, continent, start_date, end_date), fetch="one")

            result_3 = execute_query(f"""
                                    SELECT t2.Date, SUM(t2.New_recovered) AS sum_cases 
                                    FROM worldometer_data t1 
                                    INNER JOIN full_grouped t2 
                                    ON t1.Country_Region = t2.Country_Region 
                                    WHERE t1.Continent = %s 
                                    AND t2.Date >= %s 
                                    AND t2.Date <= %s 
                                    GROUP BY t2.Date 
                                    HAVING SUM(t2.New_recovered) = 
                                    ( 
                                    SELECT MAX(sub_query.daily_sum) 
                                    FROM 
                                    ( 
                                    SELECT t2.Date, SUM(t2.New_recovered) AS daily_sum 
                                    FROM worldometer_data t1 
                                    INNER JOIN full_grouped t2 
                                    ON t1.Country_Region = t2.Country_Region 
                                    WHERE t1.Continent = %s 
                                    AND t2.Date >= %s 
                                    AND t2.Date <= %s 
                                    GROUP BY t2.Date 
                                    ) AS sub_query 
                                    );    
                            """, (continent, start_date, end_date, continent, start_date, end_date), fetch="one")
            # show results
            flash(f"""{continent}'s between {start_date} and {end_date} has: 
                  <br>peak in cases at {result[0]}, where there were {result[1]} new cases
                  <br>peak in deaths at {result_2[0]}, where there were {result_2[1]} new deaths
                  <br>peak in recovered at {result_3[0]}, where there were {result_3[1]} new recovered""", "success")
            

        elif query_type == "country-sum-query":
            country = request.form.get('country-5') 
            start_date = request.form.get('start-date2')
            end_date = request.form.get('end-date2')

            result = execute_query(f""" SELECT SUM(t.New_cases) as sum
                                        FROM full_grouped t
                                        WHERE t.Date >= %s
                                        AND  t.Date <= %s
                                        AND t.Country_Region = %s;
                                        """, (start_date, end_date, country))

            result_2 = execute_query(f""" SELECT SUM(t.New_deaths) as sum
                                        FROM full_grouped t
                                        WHERE t.Date >= %s
                                        AND  t.Date <= %s
                                        AND t.Country_Region = %s;
                                        """, (start_date, end_date, country))
            result_3 = execute_query(f""" SELECT SUM(t.New_recovered) as sum
                                        FROM full_grouped t
                                        WHERE t.Date >= %s
                                        AND  t.Date <= %s
                                        AND t.Country_Region = %s;
                                        """, (start_date, end_date, country))
            # show results
            flash(f"""{country} between {start_date} and {end_date} has: 
                    <br>total cases: {int(result[0][0])}
                    <br>total deaths: {int(result_2[0][0])}
                    <br>total recovered: {int(result_3[0][0])}
                    """, "success")
            
        elif query_type == "continent-sum-query":
            continent = request.form.get('continent-3') 
            start_date = request.form.get('start-date3')
            end_date = request.form.get('end-date3')

            result = execute_query(f""" SELECT SUM(Sub.sum) AS total_cases
                                        FROM worldometer_data t
                                        INNER JOIN
                                        ( 
                                        SELECT t1.Country_Region, 
                                        SUM(t1.New_cases) as sum
                                        FROM full_grouped t1
                                        WHERE t1.Date >= %s
                                        AND  t1.Date <= %s
                                        GROUP BY t1.Country_Region
                                        ) AS Sub 
                                        ON t.Country_Region = Sub.Country_Region
                                        WHERE  t.Continent = %s
                                        GROUP BY t.Continent;
                                        """, (start_date, end_date, continent))

            result_2 = execute_query(f""" SELECT SUM(Sub.sum) AS total_cases
                                        FROM worldometer_data t
                                        INNER JOIN
                                        ( 
                                        SELECT t1.Country_Region, 
                                        SUM(t1.New_deaths) as sum
                                        FROM full_grouped t1
                                        WHERE t1.Date >= %s
                                        AND  t1.Date <= %s
                                        GROUP BY t1.Country_Region
                                        ) AS Sub 
                                        ON t.Country_Region = Sub.Country_Region
                                        WHERE  t.Continent = %s
                                        GROUP BY t.Continent;
                                        """, (start_date, end_date, continent))
            
            result_3 = execute_query(f""" SELECT SUM(Sub.sum) AS total_cases
                                        FROM worldometer_data t
                                        INNER JOIN
                                        ( 
                                        SELECT t1.Country_Region, 
                                        SUM(t1.New_recovered) as sum
                                        FROM full_grouped t1
                                        WHERE t1.Date >= %s
                                        AND  t1.Date <= %s
                                        GROUP BY t1.Country_Region
                                        ) AS Sub 
                                        ON t.Country_Region = Sub.Country_Region
                                        WHERE  t.Continent = %s
                                        GROUP BY t.Continent;
                                        """, (start_date, end_date, continent))
            # show results
            flash(f"""{continent} between {start_date} and {end_date} has: 
                    <br>total cases: {int(result[0][0])}
                    <br>total deaths: {int(result_2[0][0])}
                    <br>total recovered: {int(result_3[0][0])}
                    """, "success")

        elif query_type == "world-sum-query":
            start_date = request.form.get('start-date4')
            end_date = request.form.get('end-date4')

            result = execute_query(f""" SELECT SUM(t.New_cases) as sum
                                        FROM day_wise t
                                        WHERE t.Date >= %s
                                        AND  t.Date <= %s;
                                        """, (start_date, end_date))
            
            result_2 = execute_query(f""" SELECT SUM(t.New_deaths) as sum
                                        FROM day_wise t
                                        WHERE t.Date >= %s
                                        AND  t.Date <= %s;
                                        """, (start_date, end_date))
            
            result_3 = execute_query(f""" SELECT SUM(t.New_recovered) as sum
                                        FROM day_wise t
                                        WHERE t.Date >= %s
                                        AND  t.Date <= %s;
                                        """, (start_date, end_date))
            
            flash(f"""In the world between {start_date} and {end_date} has: 
                    <br>total cases: {int(result[0][0])}
                    <br>total deaths: {int(result_2[0][0])}
                    <br>total recovered: {int(result_3[0][0])}
                    """, "success")



        print("Flash query result:", result) # debug

        # handle output
        session['result_data'] = result
        return redirect("/query")

    return render_template("query.html", result_data = extracted_result)

# Create_Update Page
@app.route("/create_update", methods=["GET", "POST"])
def create_update():
    if request.method == "POST":

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        date = request.form.get('date')
        country = request.form.get('country')
        new_cases = request.form.get('case')

        print("update request: ", (date, country, new_cases)) # debug

        cursor.execute(f"""
                        CALL UpdateTables(%s, %s, %s);
                        """, (date, country, int(new_cases)))
        conn.commit()
        
        # Close the connection
        cursor.close()
        conn.close()

        flash(f"update successful", "success")

    return render_template("create_update.html")

# Delete Page
@app.route("/delete", methods=["GET", "POST"])
def delete():
    if request.method == "POST":

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        country = request.form.get('country')
        date = request.form.get('date')

        # real delete should not be allowed, so reset to 0.
        cursor.execute(f"""
                        CALL UpdateTables(%s, %s, %s);
                        """, (date, country, 0))
        conn.commit()
        # Close the connection
        cursor.close()
        conn.close()

        flash(f"delete successful", "success")

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
