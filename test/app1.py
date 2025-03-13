from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import mysql.connector


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Add a secret key for sessions

# Connect to MySQL
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="nari@2058",  # Replace with your MySQL password
        database="remedydb"
    )




# Route to render the login.html page
@app.route('/')
def index():
    return render_template('login.html')

# Route for the home page
@app.route('/dashboard')
def home():
    if 'username' in session:  # Check if the user is logged in
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('index'))

@app.route('/site')
def site():
    return render_template('site.html')

@app.route('/customer')
def customer():
    return render_template('customer.html')

@app.route('/userform')
def userform():
    return render_template('userform.html')

@app.route('/area')
def area():
    return render_template('area.html')

@app.route('/rows')
def rows():
    return render_template('rows.html')

@app.route('/tables')
def tables():
    return render_template('tables.html')

@app.route('/piles')
def piles():
    return render_template('pile.html')

@app.route('/assessment')
def assessment():
    return render_template('assessment.html')

@app.route('/remedy')
def remedy():
    return render_template('remedy.html')

@app.route('/inventory')
def inventory():
    return render_template('inventory.html')

@app.route('/quality')
def quality():
    return render_template('quality.html')

@app.route('/reports')
def reports():
    return render_template('reports.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/user_log')
def user_log():
    return render_template('user_log.html')

@app.route('/comments')
def comments():
    return render_template('comments.html')




# Route for user login verification
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM loginusers WHERE email = %s AND password = %s", (email, password))
    user = cursor.fetchone()

    if user:
        session['username'] = user['name']  # Store the username in the session
        return jsonify({"success": True, "message": "Login successful"})
    else:
        return jsonify({"success": False, "message": "Invalid credentials"})

# Route for user creation
@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        query = "INSERT INTO loginusers (name, email, password) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, email, password))
        connection.commit()
        return jsonify({"success": True, "message": "User created successfully"})
    except mysql.connector.Error as e:
        return jsonify({"success": False, "message": f"Error creating user: {e}"})

# Route for logging out
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)  # Remove the username from the session
    return redirect(url_for('index'))

@app.route('/submit_siteform', methods=['POST'])
def submit_siteform():
    site_name = request.form.get('site_name')
    site_location = request.form.get('location')
    site_owner = request.form.get('site_owner_name')
    site_gps = request.form.get('site_gps')

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        # Fetch the current maximum Site ID
        cursor.execute("SELECT `Site ID` FROM `Site` ORDER BY `Site ID` DESC LIMIT 1")
        result = cursor.fetchone()
        if result:
            # Extract the numeric part of the Site ID and increment it
            last_site_id = result[0]  # Example: 'S005'
            next_number = int(last_site_id[1:]) + 1  # Extract '005' and add 1
        else:
            # No entries exist; start from 1
            next_number = 1

        # Generate the new Site ID
        new_site_id = f"S{next_number:03d}"  # Format as 'S001', 'S002', etc.

        # Insert the new row with the generated Site ID
        query = """
        INSERT INTO `Site` (`Site ID`, `Cust ID`, `Site Name`, `Site Location`, `Site Owner Name`, `Site GPS`)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (new_site_id, "", site_name, site_location, site_owner, site_gps))
        connection.commit()

        return jsonify({"success": True, "message": f"Site information saved successfully with ID {new_site_id}"})
    except mysql.connector.Error as e:
        return jsonify({"success": False, "message": f"Error saving site information: {e}"})
    finally:
        cursor.close()
        connection.close()

@app.route('/submit_customerform', methods=['POST'])
def submit_customerform():
    # Getting data from the form
    name = request.form.get('name')
    address = request.form.get('address')
    contact_person = request.form.get('contact_person')
    website = request.form.get('website')
    phone_no = request.form.get('phone_no')
    country = request.form.get('country')

    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        # Fetch the current maximum Cust ID
        cursor.execute("SELECT `Cust ID` FROM `Customer` ORDER BY `Cust ID` DESC LIMIT 1")
        result = cursor.fetchone()
        if result:
            # Extract the numeric part of the Cust ID and increment it
            last_cust_id = result[0]  # Example: 'C005'
            next_number = int(last_cust_id[1:]) + 1  # Extract '005' and add 1
        else:
            # No entries exist; start from 1
            next_number = 1

        # Generate the new Cust ID
        new_cust_id = f"C{next_number:03d}"  # Format as 'C001', 'C002', etc.

        # Insert the new row with the generated Cust ID
        query = """
        INSERT INTO Customer 
        (`Cust ID`, `Customer Name`, `Customer Address`, `Contact Person`, `Customer Website`, `Phone No`, `Country`)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (new_cust_id, name, address, contact_person, website, phone_no, country))
        connection.commit()

        return jsonify({"success": True, "message": f"Customer information saved successfully with ID {new_cust_id}"})
    except mysql.connector.Error as e:
        return jsonify({"success": False, "message": f"Error saving customer information: {e}"})
    finally:
        cursor.close()
        connection.close()

@app.route('/submit_user_form', methods=['POST'])
def submit_userform():
    # Retrieve form data
    user_name = request.form.get('user_name')
    user_type = request.form.get('user_type')
    designation = request.form.get('designation')
    phone_no = request.form.get('phone_no')
    reports_to = request.form.get('reports_to')
    date_created = request.form.get('date_created')
    site_id = request.form.get('site_id')  # Get the selected Site ID

    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        # Check if the Site ID exists
        cursor.execute("SELECT `Site ID` FROM `site` WHERE `Site ID` = %s", (site_id,))
        if not cursor.fetchone():
            return jsonify({"success": False, "message": "Invalid Site ID selected."})

        # Fetch the current maximum User ID
        cursor.execute("SELECT `User ID` FROM `users` ORDER BY `User ID` DESC LIMIT 1")
        result = cursor.fetchone()
        if result and result[0]:
            last_user_id = result[0]
            next_number = int(last_user_id[1:]) + 1
        else:
            next_number = 1

        new_user_id = f"U{next_number:03d}"  # Format as 'U001', 'U002', etc.

        # Insert data into the users table
        query = """
        INSERT INTO `users` (`User ID`, `Site ID`, `User Name`, `User Type`, `User Designation`, `User Phone number`, `Reports To`, `Date Created`, `Date Removed`)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (new_user_id, site_id, user_name, user_type, designation, phone_no, reports_to, date_created, None))
        connection.commit()

        return jsonify({"success": True, "message": f"User information saved successfully with ID {new_user_id}"})
    except mysql.connector.Error as e:
        return jsonify({"success": False, "message": f"Error saving user information: {e}"})
    finally:
        cursor.close()
        connection.close()

@app.route('/submit_area_form', methods=['POST'])
def submit_area_form():
    # Retrieve form data
    location = request.form.get('location')
    gps = request.form.get('gps')

    # Validate if required fields are provided
    if not location or not gps:
        return jsonify({"success": False, "message": "All fields are required."})

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        # Fetch the current maximum Area ID
        cursor.execute("SELECT `Area ID` FROM `areas` ORDER BY `Area ID` DESC LIMIT 1")
        result = cursor.fetchone()
        
        # Determine the next Area ID
        if result and result[0]:
            last_area_id = result[0]
            next_number = int(last_area_id[1:]) + 1
        else:
            next_number = 1

        # Format the new Area ID as 'A001', 'A002', etc.
        new_area_id = f"A{next_number:03d}"

        # Insert data into the areas table with the generated Area ID
        query = """
        INSERT INTO `areas` (`Area ID`, `Location`, `GPS`)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (new_area_id, location, gps))  # Set `Area ID` as generated
        connection.commit()

        return jsonify({"success": True, "message": f"Area information saved successfully with ID {new_area_id}"})
    except mysql.connector.Error as e:
        return jsonify({"success": False, "message": f"Error saving area information: {e}"})
    finally:
        cursor.close()
        connection.close()

@app.route('/submit_user_log_form', methods=['POST'])
def submit_user_log_form():
    # Retrieve form data
    user_id = request.form.get('user_id')
    date_logged_in = request.form.get('date_logged_in')
    date_logged_out = request.form.get('date_logged_out')

    # Validate if required fields are provided
    if not user_id or not date_logged_in:
        return jsonify({"success": False, "message": "User ID and Date Logged In are required."})

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        # Insert data into the users_log table
        query = """
        INSERT INTO `user_log` (`User ID`, `Date Logged in`, `Date Logged out`)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (user_id, date_logged_in, date_logged_out))
        connection.commit()
        return jsonify({"success": True, "message": "User log information saved successfully"})
    except mysql.connector.Error as e:
        return jsonify({"success": False, "message": f"Error saving user log information: {e}"})
    finally:
        cursor.close()
        connection.close()

@app.route('/submit_comment_form', methods=['POST'])
def submit_comment_form():
    comment_type = request.form.get('comment_type')
    related_comment_id = request.form.get('related_comment_id')
    pile_id = request.form.get('pile_id')
    user_id = request.form.get('user_id')
    usage_id = request.form.get('usage_id')
    date_posted = request.form.get('date_posted')
    comment_text = request.form.get('comment_text')
    comment_date = request.form.get('comment_date')
    commented_by = request.form.get('commented_by')
    status = request.form.get('status')

    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        # Insert the data into the Comment table
        query = """
        INSERT INTO `Comments` (`Comment Type`, `Related Comment ID`, `Pile ID`, `User ID`, `Usage ID`, 
                               `Date Posted`, `Comment Text`, `Comment Date`, `Commented By`, `Status`)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (comment_type, related_comment_id, pile_id, user_id, usage_id,
                               date_posted, comment_text, comment_date, commented_by, status))
        connection.commit()
        return jsonify({"success": True, "message": "Comment information saved successfully"})
    except mysql.connector.Error as e:
        return jsonify({"success": False, "message": f"Error saving comment information: {e}"})
    finally:
        cursor.close()
        connection.close()

#connection for assessment
@app.route('/submit_task_assignment', methods=['POST'])
def submit_task_assignment():
    # Get the form data from the request
    user_id = request.form.get('user_id')
    pile_id = request.form.get('pile_id')
    task_date = request.form.get('task_date')
    allotted_date = request.form.get('allotted_date')
    allotted_by = request.form.get('allotted_by')
    date_completed = request.form.get('date_completed')
    assessment_status = request.form.get('assessment_status')
    assessment_case = request.form.get('assessment_case')
    picture_name = request.form.get('picture_name')
    picture_location = request.form.get('picture_location')

    # Establish a database connection
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        # Insert the data into the Task Assignment table
        query = """
        INSERT INTO `assessment` (`User ID`, `Pile ID`, `Task Date`, `Allotted Date`, `Allotted By`, `Date Completed`, 
                                       `Assessment Status`, `Assessment Case`, `Picture Name`, `Picture Location`)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (user_id, pile_id, task_date, allotted_date, allotted_by, date_completed, 
                               assessment_status, assessment_case, picture_name, picture_location))
        connection.commit()
        
        return jsonify({"success": True, "message": "Task assignment saved successfully"})
    except mysql.connector.Error as e:
        return jsonify({"success": False, "message": f"Error saving task assignment: {e}"})

@app.route('/submit_row_form', methods=['POST'])
def submit_row_form():
    # Get the form data
    row_id = request.form.get('row_id')
    row_name = request.form.get('row_name')
    area_id = request.form.get('area_id')
    location = request.form.get('location')
    gps = request.form.get('gps')

    # Establish DB connection
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        # Insert data into Row Information table
        query = """
        INSERT INTO `rows` (`Row ID`, `Row Name`, `Area ID`, `Location`, `GPS`)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (row_id, row_name, area_id, location, gps))
        connection.commit()

        print("Data inserted successfully")
        return jsonify({"success": True, "message": "Row information saved successfully"})

    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return jsonify({"success": False, "message": f"Error saving row information: {e}"})

@app.route('/submit_pile_form', methods=['POST'])
def submit_pile_form():
    # Get form data
    table_id = request.form.get('table_id')
    row_id = request.form.get('row_id')
    area_id = request.form.get('area_id')
    location_description = request.form.get('location_description')
    gps_location = request.form.get('gps_location')

    # Establish DB connection
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        # Insert data into Pile Form table
        query = """
        INSERT INTO `Piles` (`Table ID`, `Row ID`, `Area ID`, `Location Description`, `GPS Location`)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (table_id, row_id, area_id, location_description, gps_location))
        connection.commit()

        print("Data inserted successfully")
        return jsonify({"success": True, "message": "Pile information saved successfully"})

    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return jsonify({"success": False, "message": f"Error saving pile information: {e}"})

@app.route('/submit_table_form', methods=['POST'])
def submit_table_form():
    # Get form data
    table_id = request.form.get('table_id')
    row_id = request.form.get('row_id')
    area_id = request.form.get('area_id')
    location = request.form.get('location')
    gps = request.form.get('gps')

    # Establish DB connection
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        # Insert data into Table Form table
        query = """
        INSERT INTO `Tables` (`Table ID`, `Row ID`, `Area ID`, `Location`, `GPS`)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (table_id, row_id, area_id, location, gps))
        connection.commit()

        print("Data inserted successfully")
        return jsonify({"success": True, "message": "Table information saved successfully"})

    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return jsonify({"success": False, "message": f"Error saving table information: {e}"})

@app.route('/submit_remedy_form', methods=['POST'])
def submit_remedy_form():
    # Get form data
    user_id = request.form.get('user_id')
    pile_id = request.form.get('pile_id')
    task_date = request.form.get('task_date')
    assessed_case = request.form.get('assessed_case')
    allotted_date = request.form.get('allotted_date')
    allotted_by = request.form.get('allotted_by')
    date_completed = request.form.get('date_completed')
    remedy_status = request.form.get('remedy_status')
    remedy_text = request.form.get('remedy_text')
    picture_name = request.form.get('picture_name')
    picture_location = request.form.get('picture_location')

    # Establish DB connection
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        # Insert data into Remedy Form table
        query = """
        INSERT INTO `Remedy` (`User ID`, `Pile ID`, `Task Date`, `Assessed Case`, 
                                  `Allotted Date`, `Allotted By`, `Date Completed`, 
                                  `Remedy Status`, `Remedy Text`, `Picture Name`, `Picture Location`)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (user_id, pile_id, task_date, assessed_case, allotted_date, 
                               allotted_by, date_completed, remedy_status, remedy_text, 
                               picture_name, picture_location))
        connection.commit()

        print("Data inserted successfully")
        return jsonify({"success": True, "message": "User task information saved successfully"})

    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return jsonify({"success": False, "message": f"Error saving user task information: {e}"})

@app.route('/submit_inventory_details', methods=['POST'])
def submit_inventory_details():
    # Get form data
    item_type = request.form.get('item_type')
    item_uom = request.form.get('item_uom')
    item_desc = request.form.get('item_desc')
    item_avl_qty = request.form.get('item_avl_qty')
    item_ror = request.form.get('item_ror')
    item_value = request.form.get('item_value')
    item_rate = request.form.get('item_rate')

    # Establish DB connection
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        # Insert data into Inventory Details table
        query = """
        INSERT INTO `InventoryDetails` (`Item Type`, `Item UOM`, `Item Description`, 
                                         `Item Available Quantity`, `Item ROR`, `Item Value`, `Item Rate`)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (item_type, item_uom, item_desc, item_avl_qty, item_ror, item_value, item_rate))
        connection.commit()

        print("Data inserted successfully")
        return jsonify({"success": True, "message": "Item details saved successfully"})

    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return jsonify({"success": False, "message": f"Error saving item details: {e}"})

#invtrans
@app.route('/submit_item_transaction_form', methods=['POST'])
def submit_item_transaction_form():
    # Get form data
    item_id = request.form.get('item_id')                    
    trans_qty = request.form.get('trans_qty')                         
    trans_type = request.form.get('trans_type')
    trans_date = request.form.get('trans_date')
    user_id = request.form.get('user_id')
    usage = request.form.get('usage')

    # Establish DB connection
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        # Insert data into Item Transaction table
        query = """
        INSERT INTO `ItemTransaction` (`Item ID`, `Transaction Quantity`, `Transaction Type`, 
                                       `Transaction Date`, `User ID`, `Usage`)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (item_id, trans_qty, trans_type, trans_date, user_id, usage))
        connection.commit()

        print("Data inserted successfully")
        return jsonify({"success": True, "message": "Item transaction details saved successfully"})

    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return jsonify({"success": False, "message": f"Error saving item transaction details: {e}"})



@app.route('/get_site_ids', methods=['GET'])
def get_site_ids():
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT `Site ID`, `Site Name` FROM `site`")
        sites = [
            f"{row[1]}  " for row in cursor.fetchall()
        ]
        return jsonify({"success": True, "site_ids": sites})
    except mysql.connector.Error as e:
        return jsonify({"success": False, "message": f"Error fetching Site IDs and Site Names: {e}"})
    finally:
        cursor.close()
        connection.close()



# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)
