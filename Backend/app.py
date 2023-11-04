# Imports and DB initialization 
  
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
import datetime
from datetime import datetime
#setting an application name
app = flask.Flask(__name__) #sets up application
CORS(app) #necessary for front end code to send properly
app.config["DEBUG"] = True #allows error messages
app.secret_key = 'your_mother' #the key to the app

#connects to my MySQL database
my_creds = creds.Creds() #access my class called creds in the credy.py file
link_up = create_connection(my_creds.conString, my_creds.userName, my_creds.password, my_creds.dbName)
cursor = link_up.cursor(dictionary = True)

################################################################################################################################## GET APIS ##################################################################################################################################################

#uses the GET command to see if postman can verify the server connects
@app.route('/', methods=['GET']) #default url (http://127.0.0.1:5050/)
def home():
    return '<h1> Welcome to Sushi. </h1>' #message to confirm the code has connected with route

#example API endpoint that checks the user's role
@app.route('/rolecheck', methods=['GET'])
def rolecheck():
    current_role = request.headers.get('role') # role is in the header

    if current_role:
        if current_role == 'admin':
            return jsonify({'message': 'Admin auth'}), 200
        elif current_role == 'user':
            return jsonify({'message': 'User auth'}), 200
        elif current_role == 'editor':
            return jsonify({'message': 'Editor auth'}), 200
        else:
            return jsonify({'message': 'Role not recognized'}), 403
    else:
        return jsonify({'message': 'User not authenticated'}), 401
    
# Expire link API
@app.route('/reset-password/get/<int:link_id>', methods=['GET'])
def timelimit_link(link_id):
    cursor = link_up.cursor(dictionary=True)

    # Check is_expired value in LINK based on link_id
    cursor.execute("SELECT LINK.is_expired, ACCOUNT.account_id, ACCOUNT.username, LINK.date_added FROM LINK INNER JOIN ACCOUNT ON LINK.account_id = ACCOUNT.account_id WHERE LINK.link_id = %s", (link_id,))
    link_data = cursor.fetchone()

    if link_data:
        is_expired = link_data['is_expired']
        date_added = link_data['date_added']
        current_time = datetime.datetime.now()

        if is_expired == 1:
            # Link is expired
            return jsonify({'message': 'Link is expired'}), 400

        elif is_expired == 0:
            if date_added is not None and current_time > (date_added + datetime.timedelta(days=1)):
                # Link is expired, update is_expired to 1
                cursor.execute("UPDATE LINK SET is_expired = 1 WHERE link_id = %s", (link_id,))
                link_up.commit()
                return jsonify({'message': 'Link is expired'}), 400

            elif date_added is not None and current_time < (date_added + datetime.timedelta(days=1)):
                # Link is still valid
                return jsonify({
                    'account_id': link_data['account_id'],
                    'username': link_data['username']
                }), 200
            else:
                # Handle the case where date_added
                return jsonify({'message': 'Invalid date_added'}), 400
    else:
        # Link with the given link_id not found
        return jsonify({'message': 'Link not found'}), 404

# API to get all accounts
@app.route('/account/get-all', methods=['GET'])
def getAccountAll () :
    try:
        cursor = link_up.cursor(dictionary=True)
        cursor.execute("SELECT * FROM ACCOUNT")
        users = cursor.fetchall()


        user_list = []
        for user in users:
            user_info = {
                "account_id": user["account_id"],
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
        cursor.execute("SELECT * FROM STATE")
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
        cursor.execute("SELECT * FROM ITEM_TYPE")
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
        cursor.execute("SELECT * FROM VENDOR V JOIN STATE S ON S.state_id = V.state_id ")
        vendors = cursor.fetchall()

        vendor_list = []
        for vendor in vendors:
            vendor_info = {
                "vendor_id": vendor["vendor_id"],
                "vendor_name": vendor["vendor_name"],
                "address": vendor["address"],
                "city": vendor["city"],
                "state_id": vendor["state_id"],
                "state_abbr": vendor["state_abbr"],
                "ZIP": vendor["ZIP"],
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
    
# API to get Supply Info
@app.route('/supply/get-all', methods=['GET'])
def get_supplies():
    try:
        cursor = link_up.cursor(dictionary=True)
        cursor.execute("SELECT s.supply_id, s.item_name, s.item_type_id, it.item_type_desc, "
                       "s.vendor_id, v.vendor_name, v.contact_name, v.contact_phone, v.order_phone, v.email, v.ordering_channel, s.quantity, s.reorder_point, s.price, "
                       "s.notes, s.date_added, s.added_by, s.date_modified, s.modified_by "
                       "FROM SUPPLY s "
                       "INNER JOIN ITEM_TYPE it ON s.item_type_id = it.item_type_id "
                       "INNER JOIN VENDOR v ON s.vendor_id = v.vendor_id")
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
                "price": str(supply["price"]),
                "notes": supply["notes"],
                "date_added": supply["date_added"],
                "added_by": supply["added_by"],
                "date_modified": supply["date_modified"],
                "modified_by": supply["modified_by"],
                "contact_name": supply["contact_name"],
                "contact_phone": supply["contact_phone"],
                "order_phone": supply["order_phone"],
                "email": supply["email"],
                "ordering_channel": supply["ordering_channel"]
            }
            supply_list.append(supply_info)

        return jsonify(supply_list)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API to get price info by supply_id
@app.route('/price/<int:supply_id>', methods=['GET'])
def get_prices(supply_id):
    try:
        cursor = link_up.cursor(dictionary=True)
        query = "SELECT * FROM PRICE WHERE supply_id = %s ORDER BY modified_date ASC "
        cursor.execute(query, (supply_id,))
        prices = cursor.fetchall()

        price_list = []
        for price in prices:
            price_info = {
                "price_id": price["price_id"],
                "supply_id": price["supply_id"],
                "price": price["price"],
                "modified_date": price["modified_date"]
            }
            price_list.append(price_info)
        
        return jsonify(price_list)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

################################################################################################################################## PUT APIS ##################################################################################################################################################
# Update password and set is_updated and is_expired in LINK
@app.route('/reset-password/update', methods=['PUT'])
def update_password():
    data = request.json
    link_id = data.get('link_id')
    account_id = data.get('account_id')
    new_password = data.get('password')

    if not link_id or not account_id or not new_password:
        return jsonify({'message': 'Link ID, Account ID, and Password are required'}), 400

    # Hash the new password
    password_to_update = hashlib.sha256(new_password.encode()).hexdigest()

    # Update the password in the ACCOUNT table based on account_id
    update_account_query = "UPDATE ACCOUNT SET password = %s WHERE account_id = %s"
    cursor.execute(update_account_query, (password_to_update, account_id))
    link_up.commit()

    # Set is_updated and is_expired to 1 in LINK based on link_id
    update_link_query = "UPDATE LINK SET is_updated = 1, is_expired = 1 WHERE link_id = %s"
    cursor.execute(update_link_query, (link_id,))
    link_up.commit()

    return jsonify({'message': 'Password updated and link expired successfully'}), 200

# Update vendor information by Vendor_id
@app.route('/vendor/edit', methods=['PUT'])
def edit_vendor():
    current_role = request.headers.get('role') # role is in the header
    current_user = request.headers.get('username')
    # Check if the current user has the 'Admin' or 'Edit' role
    if current_role == 'admin' or current_role == 'editor':
        try:
            data = request.get_json()
            vendor_id = data.get('vendor_id')

            if not vendor_id:
                return jsonify({'message': 'Vendor_id is required'}), 400

            # SQL query to update the vendor in the 'VENDOR' table
            update_query = "UPDATE VENDOR SET vendor_name = %s, address = %s, city = %s, state_id = %s, ZIP = %s, " \
                        "contact_name = %s, contact_phone = %s, order_phone = %s, email = %s, ordering_channel = %s, " \
                        "notes = %s, modified_by = %s  WHERE vendor_id = %s"

            # Execute the SQL query with the provided data
            cursor.execute(update_query, (
                data.get('vendor_name'),
                data.get('address'),
                data.get('city'),
                data.get('state_id'),
                data.get('ZIP'),
                data.get('contact_name'),
                data.get('contact_phone'),
                data.get('order_phone'),
                data.get('email'),
                data.get('ordering_channel'),
                data.get('notes'),
                current_user,
                vendor_id
            ))

            # Commit the transaction to save the changes in the database
            link_up.commit()

            return jsonify({'message': 'Vendor information updated successfully'}), 200

        except Exception as e:
            # If there's an exception during the database operation, return an error message
            return jsonify({'message': f'Failed to update vendor: {str(e)}'}), 500
    else:
        return jsonify({'message': 'Permission denied'}), 403  # Forbidden

# Update supply table information by supply_id
@app.route('/supply/edit', methods=['PUT'])
def edit_supply():
    data = request.get_json()
    supply_id = data.get('supply_id')  # Receive the supply_id from the frontend
    current_role = request.headers.get('role') # role is in the header
    curerent_username = request.headers.get('username')
    new_price = data.get('price')

    if not supply_id:
        return jsonify({'message': 'supply_id is required'}), 400

    # If the current user is not authenticated, return a 401 Unauthorized response
    if current_role not in ('admin', 'editor'):
        return jsonify({'message': 'User not authenticated'}), 401

    # Check if the current user has the 'Admin' role
    if current_role == 'admin' or current_role == 'editor':
        try:       
            # SQL query to update the supply in the 'SUPPLY' table
            update_query = "UPDATE SUPPLY SET item_name = %s, item_type_id = %s, " \
                           "vendor_id = %s, reorder_point = %s, " \
                           "modified_by = %s, price = %s, notes = %s, date_modified = NOW() " \
                           "WHERE supply_id = %s"

            # Execute the SQL query with the provided data
            cursor.execute(update_query, (
                data.get('item_name'),
                data.get('item_type_id'),
                data.get('vendor_id'),
                data.get('reorder_point'),
                curerent_username,
                new_price,
                data.get('notes'),
                supply_id
            ))

            # Commit the transaction to save the changes in the 'SUPPLY' table
            link_up.commit()

            # Now, add data to the 'PRICE' table
            # Define a new SQL query to insert data into the 'PRICE' table
            price_insert_query = "INSERT INTO PRICE (supply_id, price, modified_by, modified_date) VALUES (%s, %s , %s , NOW())"

            # Execute the SQL query with the calculated values
            cursor.execute(price_insert_query, (
                supply_id,
                new_price,
                curerent_username
            ))

            # Commit the transaction for the 'PRICE' table
            link_up.commit()

            return jsonify({'message': 'Supply information updated successfully'}), 200

        except Exception as e:
            # If there's an exception during the database operation, return an error message
            return jsonify({'message': f'Failed to update supply: {str(e)}'}), 500
    else:
        return jsonify({'message': 'Permission denied'}), 403  # Forbidden

# Update account information by account_id
@app.route('/account/edit', methods=['PUT'])
def edit_account():
    current_role = request.headers.get('role') # role is in the header
    current_user = request.headers.get('username')
    # Check if the current user has the 'Admin' or 'Edit' role
    if current_role == 'admin':
        try:
            data = request.get_json()
            account_id = data.get('account_id')

            if not account_id:
                return jsonify({'message': 'account_id is required'}), 400

            # SQL query to update the vendor in the 'VENDOR' table
            update_query = "UPDATE ACCOUNT SET username = %s, password = %s, fname = %s, lname = %s, phone = %s, " \
                        "role = %s, sec_question = %s, sec_response = %s, " \
                        "date_modified = NOW() , modified_by = %s  WHERE account_id = %s"

            # Execute the SQL query with the provided data
            cursor.execute(update_query, (
                data.get('username'),
                hashlib.sha256(data.get('password').encode()).hexdigest(),
                data.get('fname'),
                data.get('lname'),
                data.get('phone'),
                data.get('role'),
                data.get('sec_question'),
                data.get('sec_response'),
                current_user,
                account_id
            ))

            # Commit the transaction to save the changes in the database
            link_up.commit()

            return jsonify({'message': 'Account information updated successfully'}), 200

        except Exception as e:
            # If there's an exception during the database operation, return an error message
            return jsonify({'message': f'Failed to update Account: {str(e)}'}), 500
    else:
        return jsonify({'message': 'Permission denied'}), 403  # Forbidden
    # Update SUPPLY table and add a new row to TRANSACTION table

@app.route('/order', methods=['PUT'])
def order():
    data = request.get_json()
    orders = data  # Assuming 'orders' is an array of objects
    current_role = request.headers.get('role') # role is in the header
    current_user = request.headers.get('username')
    if not orders:
        return jsonify({'message': 'No orders provided'}), 400

    # If the current user is not authenticated, return a 401 Unauthorized response
    if current_role not in ('admin', 'editor'):
        return jsonify({'message': 'User not authenticated'}), 401

    # Check if the current user has the 'Admin' role
    if current_role == 'admin' or current_role == 'editor':
        try:
            for order in orders:
                supply_id = order.get('supply_id')     
                qty_ordered = order.get('qty_ordered')
                quantity = order.get('quantity')
                reorder_point = order.get('reorder_point')   
                report_group = order.get('report_group')      

                # SQL query to update the SUPPLY table
                update_query = "UPDATE SUPPLY SET quantity = %s, reorder_point = %s, modified_by = %s, date_modified = NOW() " \
                               "WHERE supply_id = %s"

                # Execute the SQL query with the provided data
                cursor.execute(update_query, (
                    quantity, 
                    reorder_point,
                    current_user,
                    supply_id
                ))
                if qty_ordered>0:
                    # SQL query to add a new row to the TRANSACTION table
                    transaction_query = "INSERT INTO TRANSACTION (report_group, supply_id, modified_by, change_qty, qty_ordered, modified_date) " \
                                        "VALUES (%s,%s, %s, %s, %s, NOW())"

                    # Execute the SQL query with the calculated values
                    cursor.execute(transaction_query, (
                        report_group,
                        supply_id,
                        current_user,
                        quantity,
                        qty_ordered
                    ))

            # Commit the transaction to save the changes in the database
            link_up.commit()

            return jsonify({'message': 'Orders processed successfully'}), 200

        except Exception as e:
            # If there's an exception during the database operation, return an error message
            return jsonify({'message': f'Failed to process orders: {str(e)}'}), 500
    else:
        return jsonify({'message': 'Permission denied'}), 400

################################################################################################################################## POST APIS ##################################################################################################################################################
# Login API
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
            session_user_role = session['role']
            specific_user_role = result['role']
            specific_first_name = result['fname']
            specific_last_name = result['lname']
            return jsonify({'message': 'Login successful', 'role': specific_user_role, 'fname': specific_first_name, 'lname': specific_last_name, 'session_role': session_user_role}), 200 #return message, role, first and last name
        else:
            return jsonify({'message': 'Incorrect password'}), 401
    else:
        return jsonify({'message': 'User not found'}), 404
    
# Get security question for ACCOUNT table
@app.route('/forgotpassword', methods=['POST'])
def forgotpassword():
    data = request.get_json()
    username = data.get('username')

    if not username:
        return jsonify({'message': 'Username is required'}), 400

    try:
        cursor = link_up.cursor(dictionary=True)
        #SQL query to retrieve the security question for the given username
        cursor.execute("SELECT sec_question FROM ACCOUNT WHERE username = %s", (username,))
        security_question = cursor.fetchone()

        if security_question:
            return jsonify({'security_question': security_question['sec_question']})
        else:
            return jsonify({'message': 'Username not found'}), 404

    except Exception as e:
        #if exception
        return jsonify({'message': f'Failed to retrieve security question: {str(e)}'}), 500\


#define your email configuration for the POST "/forgotpassword/answer"
#needs to be replaced with clients email and need to make a custom app password for the client
sender_email = "rayalwayslives@gmail.com"
sender_password = "euej sysr ogto irgn" #app password for account
smtp_server = "smtp.gmail.com"
smtp_port = 587

# Check if the security password is correct for the user in the account table and if correct, add data into the LINK table
@app.route('/forgotpassword/answer', methods=['POST'])
def forgot_password_answer():
    data = request.get_json()
    username = data.get('username')
    sec_response = data.get('sec_response')
    cursor = link_up.cursor(dictionary=True)

    try:
        # SQL query to retrieve the security response for the given username
        cursor.execute("SELECT sec_response FROM ACCOUNT WHERE username = %s", (username,))
        security_response = cursor.fetchone()

        if security_response and sec_response == security_response['sec_response']:
            # Continue if security answer matches

            # Execute an SQL query to find the account_id that matches the provided username
            cursor.execute("SELECT account_id FROM ACCOUNT WHERE username = %s", (username,))
            account_id = cursor.fetchone()

            if account_id:
                # If a matching account_id is found
                account_id = account_id['account_id']

                # Insert a new row into the LINK table
                cursor.execute("INSERT INTO LINK (account_id, is_expired, is_updated) VALUES (%s, 0, 0)", (account_id,))
                link_id = cursor.lastrowid  # Get the ID of the newly added row

                # Commit the transaction to save changes to the database
                link_up.commit()

                # Send an email to the user with the reset link
                reset_link = f"https://abc?id={link_id}"

                # The code for sending the email is similar to the code you provided in the first set.
                # You can use that code to send the email here, just replace the reset link with the one you generated.
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = username
                msg['Subject'] = "Password Reset"
                message_body = f"Hello,\n\nTo reset your password, click the following link:\n{reset_link}"
                msg.attach(MIMEText(message_body, 'plain'))

                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, username, msg.as_string())
                server.quit()

                return jsonify({'message': 'Password reset email sent', 'reset_link': reset_link}), 200
            else:
                # If the username is not found in the ACCOUNT table
                return jsonify({'message': 'Unauthorized'}), 400

        else:
            # If the security response does not match
            return jsonify({'message': 'Unauthorized'}), 401

    except Exception as e:
        # Handle exceptions
        return jsonify({'message': str(e)}), 500

#Add Account 
@app.route('/account/add', methods=['POST'])
def add_account():
    # Contains JSON data
    data = request.get_json()
    current_role = request.headers.get('role') # role is in the header
    # Extract data from the request
    username = data.get('username')
    password = data.get('password')
    fname = data.get('fname')
    lname = data.get('lname')
    phone = data.get('phone')
    role = data.get('role')
    sec_question = data.get('sec_question')
    sec_response = data.get('sec_response')
    added_by = request.headers.get('username') # username is in the header


    ##### Check to see if missing info
    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    # Verify role is admin
    if current_role == 'admin':
        try:
            # Hash the password using a secure hash function like SHA-256
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            # SQL query to insert the user account into the 'ACCOUNT' table
            insert_query = "INSERT INTO ACCOUNT (username, password, fname, lname, phone, role, added_by, sec_question, sec_response, date_added) " \
                           "VALUES (%s, %s, %s, %s, %s, %s, %s,%s, %s, NOW())"

            # Execute query 
            cursor.execute(insert_query, (username, hashed_password, fname, lname, phone, role, added_by,sec_question, sec_response ))

            # Commit the transaction
            link_up.commit()

            # Get the last inserted row
            account_id = cursor.lastrowid

            # Return a JSON response with the Account_id
            return jsonify({'account_id': account_id}), 200

        except Exception as e:
            # If there's an exception during the database operation
            return jsonify({'message': f'Failed to add user account: {str(e)}'}), 500
    else:
        return jsonify({'message': 'User not authenticated'}), 401 


# Add vendor API
@app.route('/vendor/add', methods=['POST'])
def add_vendor():
    data = request.get_json()
    current_role = request.headers.get('role') # role is in the header
    vendor_name = data.get('vendor_name')
    address = data.get('address')
    city = data.get('city')
    state_id = data.get('state_id')
    ZIP = data.get('ZIP')
    contact_name = data.get('contact_name')
    contact_phone = data.get('contact_phone')
    order_phone = data.get('order_phone')
    email = data.get('email')
    ordering_channel = data.get('ordering_channel')
    notes = data.get('notes')
    added_by = request.headers.get('username') # username is in the header
 
    #if not vendor_name or not contact_name or not contact_phone or not email or not ordering_channel:
    #  return jsonify({'message': 'All fields are required'}), 400


    # If the current user is not authenticated, return a 401 Unauthorized response
    if current_role not in ('admin', 'editor'):
        return jsonify({'message': 'User not authenticated'}), 401

    
    # Check if the current user has the 'Admin' or 'Edit' role
    if current_role == 'admin' or current_role == 'editor':
        try:
            # SQL query to insert the vendor into the 'VENDOR' table
            insert_query = "INSERT INTO VENDOR (vendor_name, address, city, state_id, ZIP, contact_name, contact_phone, order_phone, email, ordering_channel, notes, added_by) " \
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

            # Execute the SQL query with the provided data
            cursor.execute(insert_query, (vendor_name, address, city, state_id, ZIP, contact_name, contact_phone, order_phone, email, ordering_channel, notes, added_by))

            # Commit the transaction to save the changes in the database
            link_up.commit()

            # Get the last inserted row's ID (Vendor_id)
            vendor_id = cursor.lastrowid

            # Return a JSON response with the Vendor_id and a 201 Created status code
            return jsonify({'Vendor_id': vendor_id}), 200

        except Exception as e:
            # If there's an exception during the database operation, return an error message
            return jsonify({'message': f'Failed to add vendor: {str(e)}'}), 500

# Add supply API
@app.route('/supply/add', methods=['POST'])
def add_supply():
    data = request.get_json()
    current_role = request.headers.get('role') # role is in the header
    item_name = data.get('item_name')
    item_type_id = data.get('item_type_id')
    vendor_id = data.get('vendor_id')
    reorder_point = data.get('reorder_point') 
    price = data.get('price')
    notes = data.get('notes')
    added_by = request.headers.get('username') # username is in the header
    date_added = datetime.now()

    if not item_name or not item_type_id or not vendor_id or not reorder_point or not added_by or not price:
        return jsonify({'message': 'All fields are required'}), 400

    # If the current user is not authenticated, return a 401 Unauthorized response
    if current_role not in ('admin', 'editor'):
        return jsonify({'message': 'User not authenticated'}), 401
    
    try:
        # SQL query to insert the supply into the 'SUPPLY' table
        supply_insert_query = "INSERT INTO SUPPLY (item_name, item_type_id, vendor_id, reorder_point, price, notes, added_by, date_added, quantity) " \
                              " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 0) "

        # Execute the SQL query with the provided data
        cursor.execute(supply_insert_query, (item_name, item_type_id, vendor_id, reorder_point, price, notes, added_by, date_added))

        # Commit the transaction to save the changes in the database
        link_up.commit()

        # Get the last inserted row's ID (Supply_id)
        supply_id = cursor.lastrowid

        # SQL query to insert price information into the 'PRICE' table
        price_insert_query = "INSERT INTO PRICE (price, supply_id, modified_by) VALUES (%s, %s, %s)"

        # Execute the SQL query with price data
        cursor.execute(price_insert_query, (price, supply_id, added_by))

        # Commit the price transaction
        link_up.commit()

        # Return a JSON response with the Supply_id and a 201 Created status code
        return jsonify({'Supply_id': supply_id}), 200

    except Exception as e:
        # If there's an exception during the database operation, return an error message
        return jsonify({'message': f'Failed to add supply: {str(e)}'}), 500
################################################################################################################################## Delete APIS ##################################################################################################################################################
    
# Account Delete
@app.route('/account/delete/<int:account_id>', methods=['DELETE'])
def delete_account(account_id):
    current_role = request.headers.get('role') # role is in the header

    # Check if the current user is logged in and has an "Admin" role
    if current_role == 'admin':
        try:
            # query to delete account from the 'ACCOUNT' table based on account_id
            delete_query = "DELETE FROM ACCOUNT WHERE account_id = %s"
            cursor.execute(delete_query, (account_id,))
            link_up.commit()

            # Check if any rows were affected by the delete operation
            if cursor.rowcount > 0:
                return jsonify({'message': 'User account deleted successfully'}), 200
            else:
                return jsonify({'message': 'User account not found'}) , 400
        except Exception as e:
            return jsonify({'message': f'Error on the backend: {str(e)}'}), 400
    else:
        return jsonify({'message': 'Unauthorized. You must be logged in as an admin to delete a user account.'}), 400
    
# Vendor Delete     
@app.route('/vendor/delete/<int:vendor_id>', methods=['DELETE'])
def delete_vendor(vendor_id):
    # Check if the current user role
    current_role = request.headers.get('role') # role is in the header
    if current_role == 'admin' or current_role == 'editor':
        try:
            # query to delete vendor from the 'VENDOR' table based on vendor_id
            delete_query = "DELETE FROM VENDOR WHERE vendor_id = %s"
            cursor.execute(delete_query, (vendor_id,))
            link_up.commit()

            # Check if any rows were affected 
            if cursor.rowcount > 0:
                return jsonify({'message': 'Vendor deleted successfully'}), 200
            else:
                return jsonify({'message': 'Vendor not found'}), 400
        except Exception as e:
            return jsonify({'message': f'Error on the backend: {str(e)}'}), 400
    else:
        return jsonify({'message': 'Unauthorized. You must be logged in as an admin or editor to delete a vendor.'}), 400
    
# Supply Delete     
@app.route('/supply/delete/<int:supply_id>', methods=['DELETE'])
def delete_supply(supply_id):
    current_role = request.headers.get('role') # role is in the header
    if current_role == 'admin' or current_role == 'editor':
        try:
            # query to delete price from the 'PRICE' table based on supply_id
            delete_query = "DELETE FROM PRICE WHERE supply_id = %s"
            cursor.execute(delete_query, (supply_id,))
            link_up.commit()

            # query to delete supply from the 'SUPPLY' table based on supply_id
            delete_query = "DELETE FROM SUPPLY WHERE supply_id = %s"
            cursor.execute(delete_query, (supply_id,))
            link_up.commit()

            # Check if any rows were affected 
            if cursor.rowcount > 0:
                return jsonify({'message': 'Vendor deleted successfully'}), 200
            else:
                return jsonify({'message': 'Vendor not found'}), 400
        except Exception as e:
            return jsonify({'message': f'Error on the backend: {str(e)}'}), 400
    else:
        return jsonify({'message': 'Unauthorized. You must be logged in as an admin or editor to delete a supply.'}), 400

if __name__ == '__main__':
    app.run(port=5050)
