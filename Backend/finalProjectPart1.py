import flask
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask
from flask import jsonify
from flask import request
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

#connects to my MySQL database
my_creds = creds.Creds() #access my class called creds in the credy.py file
link_up = create_connection(my_creds.conString, my_creds.userName, my_creds.password, my_creds.dbName)
cursor = link_up.cursor(dictionary = True)

#create user table in MySQL if not already created
user_creation_table = '''CREATE TABLE IF NOT EXISTS users (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            username VARCHAR(50) UNIQUE NOT NULL,
                            password_hash VARCHAR(128) NOT NULL,
                            role VARCHAR(50) NOT NULL
                        )'''
execute_query(link_up, user_creation_table)  # runs the SQL code on MySQL

#insert sample user data
user_data = [
    ('rayalwaysdies@gmail.com', '6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b', 'Admin'),
    ('rayalwayslives@gmail.com', 'd4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35', 'User'),
    ('yourmom@gmail.com', '4e07408562bedb8b60ce05c1decfe3ad16b72230967de01f640b7e4729b49fce', 'User')
]

for data in user_data:
    user_query = f"INSERT IGNORE INTO users (username, password_hash, role) VALUES ('{data[0]}', '{data[1]}', '{data[2]}')"
    execute_query(link_up, user_query)

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

    #query the database for the user's password hash
    cursor = link_up.cursor(dictionary=True)
    cursor.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()

    if result:
        stored_password_hash = result['password_hash']
        input_password_hash = hashlib.sha256(password.encode()).hexdigest()

        if stored_password_hash == input_password_hash:
            specific_user_role = result['role']
            return jsonify({'message': 'Login successful', 'role': specific_user_role}), 200
        else:
            return jsonify({'message': 'Incorrect password'}), 401
    else:
        return jsonify({'message': 'User not found'}), 404
    
#login creation api
@app.route('/CreateLogin', methods=['POST'])
def CreateLogin():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    #check if the username already exists in the database
    cursor = link_up.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        return jsonify({'message': 'Username already exists'}), 409

    #if the username is not taken, hash the password and insert the new user into the database
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    insert_query = "INSERT INTO users (username, password_hash) VALUES (%s, %s)"
    cursor.execute(insert_query, (username, password_hash))
    link_up.commit()

    return jsonify({'message': 'User registration successful'}), 201

#login update password api
@app.route('/ChangePassword', methods=['PUT'])
def ChangePassword():

    #gets data from JSON and assigns variables
    get_user_data = request.get_json()
    user_to_update = get_user_data.get('username')
    raw_password = get_user_data.get('password_hash')

    if not user_to_update or not raw_password:
        return jsonify({'message': 'Username and password are required'}), 400

    #hash password
    password_hash_to_update = hashlib.sha256(raw_password.encode()).hexdigest()

    #SQL gets all usernames in dict for ensuring they are actually there
    query = "Select * from users"
    cursor.execute(query)
    user_dictionary = cursor.fetchall()
    user_found = False
    for x in user_dictionary:
        #finds a matching user in users table
        if x["username"] == user_to_update:
            #SQL command to update the users table
            update_query = "UPDATE users SET password_hash = '%s' WHERE username = '%s'" % (password_hash_to_update, user_to_update)
            cursor.execute(update_query)
            link_up.commit()
            user_found = True
            return 'Successfully updated user.', 200
    if user_found == False:
        return 'User not found', 400
    
@app.route('/DeleteUser', methods=['DELETE'])
def DeleteUser():

    #gets data from JSON and assigns variables
    get_user_data = request.get_json()
    user_to_delete = get_user_data.get('username')

    if not user_to_delete:
        return jsonify({'message': 'Username is required'}), 400

    try:
        #execute the delete query with parameters
        delete_query = "DELETE FROM users WHERE username = '%s'" % (user_to_delete)
        cursor.execute(delete_query)
        link_up.commit()

        #check if any rows were affected by the delete operation
        if cursor.rowcount > 0:
            return jsonify({'message': 'User deleted successfully'}), 200
        else:
            return jsonify({'message': 'Failed to delete user'}), 400
    except Exception as e:
        return f'Error deleting user: {str(e)}', 500
    

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

if __name__ == '__main__':
    app.run(port=5050)