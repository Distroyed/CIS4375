import flask
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

# Create user table in MySQL if not already created
user_creation_table = '''CREATE TABLE IF NOT EXISTS users (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            username VARCHAR(50) UNIQUE NOT NULL,
                            password_hash VARCHAR(128) NOT NULL
                        )'''
execute_query(link_up, user_creation_table)  # runs the SQL code on MySQL

# Insert sample user data
user_data = [
    ('user1', '6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b'),
    ('user2', 'd4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35'),
    ('user3', '4e07408562bedb8b60ce05c1decfe3ad16b72230967de01f640b7e4729b49fce'),
]

for data in user_data:
    user_query = f"INSERT IGNORE INTO users (username, password_hash) VALUES ('{data[0]}', '{data[1]}')"
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
            return jsonify({'message': 'Login successful'}), 200
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

    # Check if the username already exists in the database
    cursor = link_up.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        return jsonify({'message': 'Username already exists'}), 409

    # If the username is not taken, hash the password and insert the new user into the database
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    insert_query = "INSERT INTO users (username, password_hash) VALUES (%s, %s)"
    cursor.execute(insert_query, (username, password_hash))
    link_up.commit()

    return jsonify({'message': 'User registration successful'}), 201

#login password change api
#@app.route('/LoginPasswordChange', methods=['POST'])
#def LoginPasswordChange():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    #query the database for the user's password hash
    cursor = link_up.cursor(dictionary=True)
    cursor.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()

if __name__ == '__main__':
    app.run(port=5050)