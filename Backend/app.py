# Imports and DB initialization 
  
import flask
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask_mail import Mail, Message 
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
from datetime import datetime, timedelta
#setting an application name
app = flask.Flask(__name__) #sets up application
CORS(app) #necessary for front end code to send properly
mail = Mail(app)
app.config["DEBUG"] = True #allows error messages
app.secret_key = 'your_mother' #the key to the app

#connects to my MySQL database
my_creds = creds.Creds() #access my class called creds in the credy.py file
link_up = create_connection(my_creds.conString, my_creds.userName, my_creds.password, my_creds.dbName)
cursor = link_up.cursor(dictionary = True)

# configuration of mail 
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = '7fridaysushi@gmail.com' #sponsor email
app.config['MAIL_PASSWORD'] = 'yxzr jxig gzmv whqk' #sponsor password
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app) 

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
        elif current_role == 'edit':
            return jsonify({'message': 'Edit auth'}), 200
        else:
            return jsonify({'message': 'Role not recognized'}), 403
    else:
        return jsonify({'message': 'User not authenticated'}), 401
    
# Expire link API
@app.route('/reset-password/get/<int:link_id>', methods=['GET'])
def timelimit_link(link_id):
    cursor = link_up.cursor(dictionary=True)

    # Check is_expired value in LINK based on link_id
    cursor.execute("SELECT LINK.is_expired, ACCOUNT.account_id, ACCOUNT.username, LINK.date_added, ACCOUNT.sec_question FROM LINK INNER JOIN ACCOUNT ON LINK.account_id = ACCOUNT.account_id WHERE ACCOUNT.is_available = 1 AND LINK.link_id = %s", (link_id,))
    link_data = cursor.fetchone()

    if link_data:
        is_expired = link_data['is_expired']
        date_added = link_data['date_added']
        sec_question = link_data['sec_question']
        current_time = datetime.now()

        if is_expired == 1:
            # Link is expired
            return jsonify({'message': 'Link is expired'}), 205

        elif is_expired == 0:
            if date_added is not None and current_time > (date_added + timedelta(days=1)):
                # Link is expired, update is_expired to 1
                cursor.execute("UPDATE LINK SET is_expired = 1 WHERE link_id = %s", (link_id,))
                link_up.commit()
                return jsonify({'message': 'Link is expired'}), 205

            elif date_added is not None and current_time < (date_added + timedelta(days=1)):
                # Link is still valid
                return jsonify({
                    'account_id': link_data['account_id'],
                    'sec_question' : sec_question
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
        cursor.execute("SELECT * FROM ACCOUNT WHERE is_available = 1")
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
                "sec_question": user.get("sec_question", ""), 
                "sec_response": user.get("sec_response", ""), 
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
        cursor.execute("SELECT * FROM VENDOR V JOIN STATE S ON S.state_id = V.state_id WHERE V.is_available = 1 ")
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
                       "INNER JOIN VENDOR v ON s.vendor_id = v.vendor_id "
                       "WHERE s.is_available = 1 AND v.is_available = 1")
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

#Get report history
@app.route('/report-history', methods=['GET'])
def get_grouped_data():
    try:
        cursor = link_up.cursor(dictionary=True)
        query = "SELECT T.modified_by, T.change_qty, T.modified_date, T.qty_ordered, T.report_group, S.item_name, S.price, V.vendor_name, V.contact_name, V.contact_phone, V.order_phone, V.ordering_channel, V.email FROM TRANSACTION T JOIN SUPPLY S ON T.supply_id = S.supply_id JOIN VENDOR V on V.vendor_id = S.vendor_id WHERE S.is_available = 1 AND V.is_available = 1"
        cursor.execute(query)
        data = cursor.fetchall()

        grouped_data = {}
        for row in data:
            report_group = row['report_group']
            if report_group not in grouped_data:
                grouped_data[report_group] = []
            grouped_data[report_group].append(row)

        result = [{'report_group': key, 'data': value} for key, value in grouped_data.items()]

        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)})

# API to get price info by supply_id
@app.route('/pie-chart', methods=['GET'])
def get_chart_data():
    try:
        cursor = link_up.cursor(dictionary=True)
        query = "SELECT V.vendor_id, V.vendor_name, COUNT(*) AS supply_count FROM SUPPLY S JOIN VENDOR V ON S.vendor_id = V.vendor_id WHERE V.is_available = 1 AND S.is_available = 1 GROUP BY vendor_id;"
        cursor.execute(query)
        data = cursor.fetchall()

        chart_data = []
        for each in data:
            chart_data_info = {
                "name": each["vendor_name"],
                "value": each["supply_count"]
            }
            chart_data.append(chart_data_info)
        
        return jsonify(chart_data)
    
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

    # Check is_expired value in LINK based on link_id
    cursor.execute("SELECT username FROM ACCOUNT WHERE account_id = %s AND is_available = 1", (account_id,))
    username_result = cursor.fetchone()

    if username_result is not None:
        username = username_result[0]
    else:
        return jsonify({'message': 'No matched account found'}), 400
    
    # Hash the new password
    password_to_update = hashlib.sha256(new_password.encode()).hexdigest()

    # Update the password in the ACCOUNT table based on account_id
    update_account_query = "UPDATE ACCOUNT SET password = %s, date_modified = NOW(), modified_by = %s WHERE account_id = %s"
    cursor.execute(update_account_query, (password_to_update, username, account_id))
    link_up.commit()

    # Set is_updated and is_expired to 1 in LINK based on link_id
    update_link_query = "UPDATE LINK SET is_updated = 1, is_expired = 1, date_modified = NOW() WHERE link_id = %s"
    cursor.execute(update_link_query, (link_id,))
    link_up.commit()

    return jsonify({'message': 'Password updated and link expired successfully'}), 200

# Update vendor information by Vendor_id
@app.route('/vendor/edit', methods=['PUT'])
def edit_vendor():
    current_role = request.headers.get('role') # role is in the header
    current_user = request.headers.get('username')
    # Check if the current user has the 'Admin' or 'Edit' role
    if current_role == 'admin' or current_role == 'edit':
        try:
            data = request.get_json()
            vendor_id = data.get('vendor_id')
            vendor_name = data.get('vendor_name')
            if not vendor_id:
                return jsonify({'message': 'Vendor_id is required'}), 400

            test_query = "SELECT * FROM VENDOR WHERE vendor_name = %s AND vendor_id != %s"
            cursor.execute(test_query, (vendor_name, vendor_id,))
            # Fetch the result
            result = cursor.fetchone()
            if result is not None:
                return jsonify({'message' : 'Duplicate Vendor Name'}), 415
            
            # SQL query to update the vendor in the 'VENDOR' table
            update_query = "UPDATE VENDOR SET vendor_name = %s, address = %s, city = %s, state_id = %s, ZIP = %s, " \
                        "contact_name = %s, contact_phone = %s, order_phone = %s, email = %s, ordering_channel = %s, " \
                        "notes = %s, modified_by = %s  WHERE vendor_id = %s AND is_available = 1 "

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
    if current_role not in ('admin', 'edit'):
        return jsonify({'message': 'User not authenticated'}), 401

    # Check if the current user has the 'Admin' role
    if current_role == 'admin' or current_role == 'edit':
        try:       
            # SQL query to update the supply in the 'SUPPLY' table
            update_query = "UPDATE SUPPLY SET item_name = %s, item_type_id = %s, " \
                           "vendor_id = %s, reorder_point = %s, " \
                           "modified_by = %s, price = %s, notes = %s, date_modified = NOW() " \
                           "WHERE supply_id = %s AND is_available = 1 "

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
    if current_role == 'admin' or current_role == 'edit':
        try:
            data = request.get_json()
            account_id = data.get('account_id')
            username = data.get('username')
            if not account_id:
                return jsonify({'message': 'account_id is required'}), 400
            
            test_query = "SELECT * FROM ACCOUNT WHERE username = %s AND account_id != %s"
            cursor.execute(test_query, (username, account_id,))
            # Fetch the result
            result = cursor.fetchone()
            if result is not None:
                return jsonify({'message' : 'Duplicate Account Username - Email'}), 415
            
            # Check if password is provided
            if 'password' in data:
                password = hashlib.sha256(data['password'].encode()).hexdigest()
            else:
                password = None

            # SQL query to update the account in the 'ACCOUNT' table
            update_query = "UPDATE ACCOUNT SET "
            if password is not None:
                update_query += "password = %s, "
            
            update_query += "username = %s, fname = %s, lname = %s, phone = %s, role = %s, " \
                           "sec_question = %s, sec_response = %s, " \
                           "date_modified = NOW(), modified_by = %s " \
                           "WHERE account_id = %s AND is_available = 1"
            
            # Build a list of values to update
            values = []
            
            if password is not None:
                values.append(password)
            
            values.extend([data.get('username'),data.get('fname'), data.get('lname'), data.get('phone'),
                           data.get('role'), data.get('sec_question'), data.get('sec_response'),
                           current_user, account_id])
            
            # Execute the SQL query with the provided data
            cursor.execute(update_query, values)
            
            # Commit the transaction to save the changes in the database
            link_up.commit()

            return jsonify({'message': 'Account information updated successfully'}), 200

        except Exception as e:
            # If there's an exception during the database operation, return an error message
            return jsonify({'message': f'Failed to update Account: {str(e)}'}), 500
    else:
        return jsonify({'message': 'Permission denied'}), 403  # Forbidden
    
@app.route('/order', methods=['PUT'])
def order():
    data = request.get_json()
    orders = data  # Assuming 'orders' is an array of objects
    current_role = request.headers.get('role') # role is in the header
    current_user = request.headers.get('username')
    if not orders:
        return jsonify({'message': 'No orders provided'}), 400

    # If the current user is not authenticated, return a 401 Unauthorized response
    if current_role not in ('admin', 'edit'):
        return jsonify({'message': 'User not authenticated'}), 401

    # Check if the current user has the 'Admin' role
    if current_role == 'admin' or current_role == 'edit':
        try:
            for order in orders:
                supply_id = order.get('supply_id')     
                qty_ordered = order.get('qty_ordered')
                quantity = order.get('quantity')
                reorder_point = order.get('reorder_point')   
                report_group = order.get('report_group')      

                # SQL query to update the SUPPLY table
                update_query = "UPDATE SUPPLY SET quantity = %s, reorder_point = %s, modified_by = %s, date_modified = NOW() " \
                               "WHERE supply_id = %s AND is_available = 1"

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
            msg = Message( 
                '7Friday Sushi - A new report has been generated', 
                sender ='7fridaysushi@gmail.com',  
                recipients = 'vnguyen@7fridaysushi.com' 
               ) 
            msg.body = f"Hello Nguyen,\n\n A new report has been generated with ID: {report_group} by {current_user}. \n\nNotice: This is just a notification, please use the application to view the report detail!"
            mail.send(msg) 
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
    cursor.execute("SELECT password, role, fname, lname FROM ACCOUNT WHERE username = %s AND is_available = 1", (username,))
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
        cursor.execute("SELECT account_id, fname, lname FROM ACCOUNT WHERE username = %s AND is_available = 1", (username,))
        result = cursor.fetchone()
        account_id = result['account_id']
        fname = result['fname']
        lname = result['lname']

        if account_id:
            # Insert a new row into the LINK table
            cursor.execute("INSERT INTO LINK (account_id, is_expired, is_updated, date_added) VALUES (%s, 0, 0, NOW())", (account_id,))
            link_id = cursor.lastrowid  # Get the ID of the newly added row

            # Commit the transaction to save changes to the database
            link_up.commit()

            # Send an email to the user with the reset link http://localhost:3000/reset-password/{link_id}
            reset_link = f'http://7fridaysushi-inventory-frontend.s3-website.us-east-2.amazonaws.com/reset-password?id={link_id}' 

            # The code for sending the email is similar to the code you provided in the first set.
            msg = Message( 
                '7Friday Sushi - Reset Password', 
                sender ='7fridaysushi@gmail.com',  #should be the sponsor email address
                recipients = [username] 
               ) 
            msg.body = f"Hello {fname} {lname},\n\nTo reset your password, click on the following link and follow instruction :\n{reset_link} \nThis link will be expired in 1 day. \n\nNotice: If you did not request to reset your password, please ignore this email and report to your admin!"
            mail.send(msg) 
            return jsonify({'message': 'Password reset email sent'}), 200            
        else:
            return jsonify({'message': 'Username not found'}), 205

    except Exception as e:
        #if exception
        return jsonify({'message': f'Failed to send reset password email: {str(e)}'}), 500


# Check if the security password is correct for the user in the account table and if correct, add data into the LINK table
@app.route('/forgotpassword/answer', methods=['POST'])
def forgot_password_answer():
    data = request.get_json()
    sec_response = data.get('sec_response')
    account_id = data.get('account_id')

    cursor = link_up.cursor(dictionary=True)

    try:
        # SQL query to retrieve the security response for the given username
        cursor.execute("SELECT username, sec_response FROM ACCOUNT WHERE account_id = %s AND is_available = 1", (account_id,))
        result  = cursor.fetchone()
        username = result['username']
        security_response_db = result['sec_response']

        if security_response_db and sec_response == security_response_db:
            update_query1 = "UPDATE ACCOUNT SET password=%s, date_modified = NOW(), modified_by = %s WHERE account_id = %s"
            cursor.execute(update_query1, (
                hashlib.sha256(data.get('password').encode()).hexdigest(),
                username,
                data.get('account_id')
            ))
            link_up.commit()
            update_query2 = "UPDATE LINK SET is_expired = 1, is_updated = 1, date_modified = NOW() WHERE link_id = %s"
            cursor.execute(update_query2, (
                data.get('link_id'),
            ))
            link_up.commit()        
            return jsonify({'message': 'Password Updated Successfully'}), 200
        else:
            # If the security response does not match
            return jsonify({'message': 'Wrong Response'}), 205

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
            test_query = "SELECT * FROM ACCOUNT WHERE username = %s"
            cursor.execute(test_query, (username,))
            # Fetch the result
            result = cursor.fetchone()
            if result is not None:
                return jsonify({'message' : 'Duplicate Account Username - Email'}), 415
            
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
    if current_role not in ('admin', 'edit'):
        return jsonify({'message': 'User not authenticated'}), 401

    
    # Check if the current user has the 'Admin' or 'Edit' role
    if current_role == 'admin' or current_role == 'edit':
        try:
            test_query = "SELECT * FROM VENDOR WHERE vendor_name = %s"
            cursor.execute(test_query, (vendor_name,))
            # Fetch the result
            result = cursor.fetchone()
            if result is not None:
                return jsonify({'message' : 'Duplicate Vendor Name'}), 415

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
    if current_role not in ('admin', 'edit'):
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
@app.route('/account/delete', methods=['PUT'])
def delete_account():
    current_role = request.headers.get('role') # role is in the header
    current_user = request.headers.get('username')
    print(current_role)
    # Check if the current user is logged in and has an "Admin" role
    if current_role == 'admin':
        try:
            # query to delete account from the 'ACCOUNT' table based on account_id
            # delete_query = "DELETE FROM ACCOUNT WHERE account_id = %s"
            #cursor.execute(delete_query, (account_id,))
            #link_up.commit() """

            # Check if any rows were affected by the delete operation
            # if cursor.rowcount > 0:
            #    return jsonify({'message': 'User account deleted successfully'}), 200
            #else:
            #    return jsonify({'message': 'User account not found'}) , 400 """
            account_id = int(request.data)
            if not account_id:
                return jsonify({'message': 'account_id is required'}), 400
            #Soft Delete
            soft_delete = "UPDATE ACCOUNT SET is_available = 0, date_modified = NOW(), modified_by = %s WHERE account_id = %s"
            cursor.execute(soft_delete, (current_user, account_id))
            return jsonify({'message': 'User account deleted successfully'}), 200
        
        except Exception as e:
            return jsonify({'message': f'Error on the backend: {str(e)}'}), 400
    else:
        return jsonify({'message': 'Unauthorized. You must be logged in as an admin to delete a user account.'}), 450
    
# Vendor Delete     
@app.route('/vendor/delete', methods=['PUT'])
def delete_vendor():
    # Check if the current user role
    current_role = request.headers.get('role') # role is in the header
    current_user = request.headers.get('username')
    if current_role == 'admin' or current_role == 'edit':
        try:
            # query to delete vendor from the 'VENDOR' table based on vendor_id
            # delete_query = "DELETE FROM VENDOR WHERE vendor_id = %s"
            #cursor.execute(delete_query, (vendor_id,))
            #link_up.commit() """

            # Check if any rows were affected 
            #if cursor.rowcount > 0:
            #    return jsonify({'message': 'Vendor deleted successfully'}), 200
            #else:
            #    return jsonify({'message': 'Vendor not found'}), 400 """
            vendor_id = int(request.data)
            if not vendor_id:
                return jsonify({'message': 'Vendor_id is required'}), 400
            #Soft Delete
            soft_delete = "UPDATE VENDOR SET is_available = 0, date_modified = NOW(), modified_by = %s WHERE vendor_id = %s"
            cursor.execute(soft_delete, (current_user, vendor_id))
            return jsonify({'message': 'Vendor profile deleted successfully'}), 200
        
        except Exception as e:
            return jsonify({'message': f'Error on the backend: {str(e)}'}), 400
    else:
        return jsonify({'message': 'Unauthorized. You must be logged in as an admin or edit to delete a vendor.'}), 450
    
# Supply Delete     
@app.route('/supply/delete', methods=['PUT'])
def delete_supply():
    current_role = request.headers.get('role') # role is in the header
    current_user = request.headers.get('username')
    print(current_role)
    if current_role == 'admin' or current_role == 'edit':
        try:
            # query to delete price from the 'PRICE' table based on supply_id
            # delete_query = "DELETE FROM PRICE WHERE supply_id = %s"
            #cursor.execute(delete_query, (supply_id,))
            #link_up.commit() """

            # query to delete supply from the 'SUPPLY' table based on supply_id
            # delete_query = "DELETE FROM SUPPLY WHERE supply_id = %s"
            #cursor.execute(delete_query, (supply_id,))
            #link_up.commit() """

            # Check if any rows were affected 
            # if cursor.rowcount > 0:
            #    return jsonify({'message': 'Vendor deleted successfully'}), 200
            #else:
            #   return jsonify({'message': 'Vendor not found'}), 400 """
            supply_id = int(request.data)
            if not supply_id:
                return jsonify({'message': 'supply_id is required'}), 400
            #Soft Delete
            soft_delete = "UPDATE SUPPLY SET is_available = 0, date_modified = NOW(), modified_by = %s WHERE supply_id = %s"
            cursor.execute(soft_delete, (current_user, supply_id))
            return jsonify({'message': 'Supply profile deleted successfully'}), 200
        
        except Exception as e:
            return jsonify({'message': f'Error on the backend: {str(e)}'}), 400
    else:
        return jsonify({'message': 'Unauthorized. You must be logged in as an admin or edit to delete a supply.'}), 450

if __name__ == '__main__':
    app.run(port=5050)
