import flask
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask
from flask import jsonify
from flask import request
from flask import session
from flask import redirect
from flask import url_for
from flask_cors import CORS
from sql import create_connection
from sql import execute_read_query
from sql import execute_query
import creds
import hashlib

#setting an application name
app = flask.Flask(__name__) #sets up application
CORS(app) #necessary for front end code to send properly
app.config["DEBUG"] = True #allows error messages
app.secret_key = 'your_mother' #the key to the app

#connects to my MySQL database
my_creds = creds.Creds() #access my class called creds in the credy.py file
link_up = create_connection(my_creds.conString, my_creds.userName, my_creds.password, my_creds.dbName)
cursor = link_up.cursor(dictionary = True)

# Create the "ACCOUNT" table if not already created
account_creation_table = '''
    CREATE TABLE IF NOT EXISTS ACCOUNT (
        account_id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        fname VARCHAR(100),
        lname VARCHAR(100),
        email VARCHAR(255),
        phone VARCHAR(20),
        role VARCHAR(50),
        sec_question TEXT,
        sec_response TEXT,
        date_added DATE,
        added_by VARCHAR(255),
        date_modified DATE,
        modified_by VARCHAR(255)
    )
'''

# Execute the SQL code to create the table
execute_query(link_up, account_creation_table)

# Insert sample user data
account_data = [
    ('rayalwaysdies@gmail.com', '6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b', 'John', 'Doe', 'rayalwaysdies@gmail.com', '1234567890', 'admin', 'What is?', 'Blue', '2023-10-09', 'AdminUser', '2023-10-09', 'AdminUser'),
    ('rayalwayslives@gmail.com', 'd4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35', 'Jane', 'Smith', 'rayalwayslives@gmail.com', '9876543210', 'user', 'What is?', 'Fluffy', '2023-10-09', 'AdminUser', '2023-10-09', 'AdminUser'),
    ('yourmom@gmail.com', '4e07408562bedb8b60ce05c1decfe3ad16b72230967de01f640b7e4729b49fce', 'Alice', 'Johnson', 'yourmom@gmail.com', '5555555555', 'user', 'What is?', 'Smith', '2023-10-09', 'AdminUser', '2023-10-09', 'AdminUser')
]

# Loop through user_data and insert it into the table
for data in account_data:
    account_query = user_query = f'''
    INSERT IGNORE INTO ACCOUNT (username, password, fname, lname, email, phone, role, sec_question, sec_response, date_added, added_by, date_modified, modified_by)
    VALUES ('{data[0]}', '{data[1]}', '{data[2]}', '{data[3]}', '{data[4]}', '{data[5]}', '{data[6]}', '{data[7]}', '{data[8]}', '{data[9]}', '{data[10]}', '{data[11]}', '{data[12]}')
'''
    # Execute the query with data from the current user
    execute_query(link_up, account_query)


#uses the GET command to see if postman can verify the server connects
@app.route('/', methods=['GET']) #default url (http://127.0.0.1:5050/)
def home():
    return '<h1> Welcome to the memes. </h1>' #message to confirm the code has connected with route

#login api
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    #query the database for the ACCOUNT password hash
    cursor = link_up.cursor(dictionary=True)
    cursor.execute("SELECT password, role, fname, lname FROM ACCOUNT WHERE username = %s", (username,))
    result = cursor.fetchone()

    if result:
        stored_password_hash = result['password']
        input_password_hash = hashlib.sha256(password.encode()).hexdigest()

        if stored_password_hash == input_password_hash:
            session['username'] = username
            session['role'] = result['role']
            specific_user_role = result['role']
            specific_first_name = result['fname']
            specific_last_name = result['lname']
            return jsonify({'message': 'Login successful', 'role': specific_user_role, 'fname': specific_first_name, 'lname': specific_last_name}), 200 #return message, role, first and last name
        else:
            return jsonify({'message': 'Incorrect password'}), 401
    else:
        return jsonify({'message': 'User not found'}), 404

#example API endpoint that checks the user's role
@app.route('/rolecheck', methods=['GET'])
def rolecheck():
    user_role = session.get('role')

    if user_role:
        if user_role == 'admin':
            return jsonify({'message': 'Admin auth'}), 200
        elif user_role == 'user':
            return jsonify({'message': 'User auth'}), 200
        else:
            return jsonify({'message': 'Role not recognized'}), 403
    else:
        return jsonify({'message': 'User not authenticated'}), 401
    
#login creation api
@app.route('/CreateLogin', methods=['POST'])
def CreateLogin():
    # Check if the user is logged in and has an "Admin" role in the session
    if 'username' in session and 'role' in session and session['role'] == 'admin':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'message': 'Username and password are required'}), 400

        #check if the username already exists in the database
        cursor = link_up.cursor(dictionary=True)
        cursor.execute("SELECT * FROM ACCOUNT WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            return jsonify({'message': 'Username already exists'}), 409

        # If the username is not taken, hash the password and insert the new user into the database
        password = hashlib.sha256(password.encode()).hexdigest()
        insert_query = "INSERT INTO ACCOUNT (username, password) VALUES (%s, %s)"
        cursor.execute(insert_query, (username, password))
        link_up.commit()

        return jsonify({'message': 'User registration successful'}), 200
    
    else:
        return jsonify({'message': 'Unauthorized. You must be logged in as an admin to create a new login.'}), 401

#login update password api #add security password #verify if link is expired
@app.route('/reset-password/update', methods=['PUT'])
def update():
    # Gets data from JSON and assigns variables
    get_user_data = request.get_json()
    user_to_update = get_user_data.get('username')
    raw_password = get_user_data.get('password')

    if not user_to_update or not raw_password:
        return jsonify({'message': 'Username and password are required'}), 400

    # Hash the password
    password_to_update = hashlib.sha256(raw_password.encode()).hexdigest()

    # SQL gets all usernames in dict for ensuring they are actually there
    query = "SELECT * FROM ACCOUNT"
    cursor.execute(query)
    user_dictionary = cursor.fetchall()
    user_found = False

    for user in user_dictionary:
        # Finds a matching user in the ACCOUNT table
        if user["username"] == user_to_update:
            # SQL command to update the user's password
            update_query = "UPDATE ACCOUNT SET password = %s WHERE username = %s"
            cursor.execute(update_query, (password_to_update, user_to_update))
            link_up.commit()
            user_found = True
            return jsonify({'message': 'User password updated successfully'}), 200

    if not user_found:
        return jsonify({'message': 'User not found'}), 404
    
@app.route('/DeleteUser', methods=['DELETE'])
def DeleteUser():
    # Check if the user is logged in and has an "Admin" role in the session
    if 'username' in session and 'role' in session and session['role'] == 'admin':
        #gets data from JSON and assigns variables
        get_user_data = request.get_json()
        user_to_delete = get_user_data.get('username')

        if not user_to_delete:
            return jsonify({'message': 'Username is required'}), 400

        try:
            # Execute the delete query with parameters
            delete_query = "DELETE FROM ACCOUNT WHERE username = %s"
            cursor.execute(delete_query, (user_to_delete,))
            link_up.commit()

            #check if any rows were affected by the delete operation
            if cursor.rowcount > 0:
                return jsonify({'message': 'User deleted successfully'}), 200
            else:
                return jsonify({'message': 'Failed to delete user'}), 400
        except Exception as e:
            return jsonify({'message': 'Error on backend'}), 500
    else:
        return jsonify({'message': 'You do not have permission to delete users'}), 403  #auth
    

#define your email configuration
#needs to be replaced with clients email and need to make a custom app password for the client
sender_email = "rayalwayslives@gmail.com"
sender_password = "euej sysr ogto irgn" #app password for account
smtp_server = "smtp.gmail.com"
smtp_port = 587

#forgot password api
@app.route('/ForgotPassword', methods=['GET'])
def ForgotPassword():
    #gets data from JSON and assigns variables
    data = request.get_json()
    username = data.get('username')

    #check if the username already exists in the database
    cursor = link_up.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    existing_user = cursor.fetchone()

    #check if username is provided and in database
    if not existing_user:
        return jsonify({'message': 'Username field invalid'}), 400
    
    try:
        # Create a message object
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = username  
        msg['Subject'] = "Password Reset"

        #generate a password reset link (you should replace this with your actual reset link)
        reset_link = "http://127.0.0.1:5050/ChangePassword"
        message_body = f"Hello,\n\nTo reset your password, click the following link:\n{reset_link}"

        #attach the message body to the email
        msg.attach(MIMEText(message_body, 'plain'))

        #connect to the SMTP server and send the email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, username, msg.as_string())
        server.quit()
        return jsonify({'message': 'Password reset email sent'}), 200
    
    except Exception as e:
        error_message = str(e)
        return jsonify({'message': 'Failed to send password reset email', 'error': error_message}), 500

######################Freeborn Code##################################

# Add vendor API
@app.route('/vendor/add', methods=['POST'])
def add_vendor():
    data = request.get_json()
    vendor_name = data.get('vendor_name')
    address = data.get('address')
    city = data.get('city')
    state_abbr = data.get('state_abbr')
    ZIP = data.get('ZIP')
    contact_name = data.get('contact_name')
    contact_phone = data.get('contact_phone')
    order_phone = data.get('order_phone')
    email = data.get('email')
    ordering_channel = data.get('ordering_channel')
    notes = data.get('notes')
  


    if not vendor_name or not address or not city or not state_abbr or not ZIP or not contact_name or not contact_phone or not order_phone or not email or not ordering_channel:
        return jsonify({'message': 'All fields are required'}), 400


    # If the current user is not authenticated, return a 401 Unauthorized response
    if 'username' in session and 'role' in session and session['role'] != 'admin':
        return jsonify({'message': 'User not authenticated'}), 401

    
    # Check if the current user has the 'Admin' or 'Edit' role
    if 'username' in session and 'role' in session and session['role'] == 'admin':
        try:
            # SQL query to insert the vendor into the 'VENDOR' table
            insert_query = "INSERT INTO VENDOR (vendor_name, address, city, state_abbr, ZIP, contact_name, contact_phone, order_phone, email, ordering_channel, notes, added_by) " \
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

            # Execute the SQL query with the provided data
            cursor.execute(insert_query, (vendor_name, address, city, state_abbr, ZIP, contact_name, contact_phone, order_phone, email, ordering_channel, notes, current_user_username))

            # Commit the transaction to save the changes in the database
            link_up.commit()

            # Get the last inserted row's ID (Vendor_id)
            vendor_id = cursor.lastrowid

            # Return a JSON response with the Vendor_id and a 201 Created status code
            return jsonify({'Vendor_id': vendor_id}), 201

        except Exception as e:
            # If there's an exception during the database operation, return an error message
            return jsonify({'message': f'Failed to add vendor: {str(e)}'}), 500

# Add supply API
@app.route('/supply/add', methods=['POST'])
def add_supply():
    data = request.get_json()
    item_name = data.get('item_name')
    item_type_id = data.get('item_type_id')
    item_type_desc = data.get('item_type_desc')
    vendor_id = data.get('vendor_id')
    reorder_point = data.get('reorder_point')
    added_by = data.get('added_by')
    price = data.get('price')
 
    

    if not item_name or not item_type_id or not item_type_desc or not vendor_id or not reorder_point or not added_by or not price:
        return jsonify({'message': 'All fields are required'}), 400

    

    if 'username' in session and 'role' in session and session['role'] != 'admin':
        return jsonify({'message': 'Only Admins or Editors can add supplies'}), 403
    
    try:
        # SQL query to insert the supply into the 'SUPPLY' table
        supply_insert_query = "INSERT INTO SUPPLY (item_name, item_type_id, item_type_desc, vendor_id, reorder_point, added_by) " \
                              "VALUES (%s, %s, %s, %s, %s, %s)"

        # Execute the SQL query with the provided data
        cursor.execute(supply_insert_query, (item_name, item_type_id, item_type_desc, vendor_id, reorder_point, added_by))

        # Commit the transaction to save the changes in the database
        link_up.commit()

        # Get the last inserted row's ID (Supply_id)
        supply_id = cursor.lastrowid

        # SQL query to insert price information into the 'PRICE' table
        price_insert_query = "INSERT INTO PRICE (price, supply_id, added_by) VALUES (%s, %s, %s)"

        # Execute the SQL query with price data
        cursor.execute(price_insert_query, (price, supply_id, added_by))

        # Commit the price transaction
        link_up.commit()

        # Return a JSON response with the Supply_id and a 201 Created status code
        return jsonify({'Supply_id': supply_id}), 201

    except Exception as e:
        # If there's an exception during the database operation, return an error message
        return jsonify({'message': f'Failed to add supply: {str(e)}'}), 500\

######################Cesar Code##################################
# API to get all accounts
@app.route('/account/get-all', methods=['GET'])
def getAccountAll () :
    try:
        cursor = link_up.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()


        user_list = []
        for user in users:
            user_info = {
                "account_id": user["id"],
                "username": user["username"],
                "fname": user.get("fname", ""),  
                "lname": user.get("lname", ""),  
                "phone": user.get("phone", ""),  
                "role": user["role"],
                "date_added": user.get("date_added", ""),  
                "added_by": user.get("added_by", ""),  
                "date_modified": user.get("date_modified", ""),  
                "modified_by": user.get("modified_by", ""),  
            }
            user_list.append(user_info)

        return jsonify(user_list)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

# API to get state
@app.route('/states', methods=['GET'])
def getStates():
    try:
        cursor = link_up.cursor(dictionary=True)
        cursor.execute("SELECT * FROM states")
        states = cursor.fetchall()


        state_list = []
        for state in states:
            state_info = {
                "state_id": state["state_id"],
                "state_name": state["state_name"],
                "state_abbr": state["state_abbr"]
            }
            state_list.append(state_info)

        return jsonify(state_list)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# API to get all item types
@app.route('/item-type/get-all', methods=['GET'])
def getAllItemType():
    try:
        cursor = link_up.cursor(dictionary=True)
        cursor.execute("SELECT * FROM item_types")
        item_types = cursor.fetchall()

        item_type_list = []
        for item_type in item_types:
            item_type_info = {
                "item_type_id": item_type["item_type_id"],
                "item_type_desc": item_type["item_type_desc"]
            }
            item_type_list.append(item_type_info)

        return jsonify(item_type_list)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# API to get vendor info
@app.route('/vendor/get-all', methods=['GET'])
def get_vendors():
    try:
        cursor = link_up.cursor(dictionary=True)
        cursor.execute("SELECT * FROM vendors")
        vendors = cursor.fetchall()

        vendor_list = []
        for vendor in vendors:
            vendor_info = {
                "vendor_id": vendor["vendor_id"],
                "vendor_name": vendor["vendor_name"],
                "address": vendor["address"],
                "city": vendor["city"],
                "state_abbr": vendor["state_abbr"],
                "zip": vendor["zip"],
                "contact_name": vendor["contact_name"],
                "contact_phone": vendor["contact_phone"],
                "order_phone": vendor["order_phone"],
                "email": vendor["email"],
                "ordering_channel": vendor["ordering_channel"],
                "notes": vendor["notes"],
                "date_added": vendor["date_added"],
                "added_by": vendor["added_by"],
                "date_modified": vendor["date_modified"],
                "modified_by": vendor["modified_by"]
            }
            vendor_list.append(vendor_info)
        
        return jsonify(vendor_list)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/supply/get-all', methods=['GET'])
def get_supplies():
    try:
        cursor = link_up.cursor(dictionary=True)
        cursor.execute("SELECT s.supply_id, s.item_name, s.item_type_id, it.item_type_desc, "
                       "s.vendor_id, v.vendor_name, s.quantity, s.reorder_point, s.price, "
                       "s.notes, s.date_added, s.added_by, s.date_modified, s.modified_by "
                       "FROM supplies s "
                       "INNER JOIN item_types it ON s.item_type_id = it.item_type_id "
                       "INNER JOIN vendors v ON s.vendor_id = v.vendor_id")
        supplies = cursor.fetchall()

        supply_list = []
        for supply in supplies:
            supply_info = {
                "supply_id": supply["supply_id"],
                "item_name": supply["item_name"],
                "item_type_id": supply["item_type_id"],
                "item_type_desc": supply["item_type_desc"],
                "vendor_id": supply["vendor_id"],
                "vendor_name": supply["vendor_name"],
                "quantity": supply["quantity"],
                "reorder_point": supply["reorder_point"],
                "price": supply["price"],
                "notes": supply["notes"],
                "date_added": supply["date_added"],
                "added_by": supply["added_by"],
                "date_modified": supply["date_modified"],
                "modified_by": supply["modified_by"]
            }
            supply_list.append(supply_info)

        return jsonify(supply_list)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5050)