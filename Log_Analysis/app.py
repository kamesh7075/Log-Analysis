from flask import Flask, request, render_template, jsonify
import logging
import os

app = Flask(__name__)

# Set up logging
log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app.log')
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    ip_address = request.remote_addr  # Get the client's IP address

    # Log the login attempt with IP
    logging.info(f"Login attempt: Username: {username}, Password: {password}, IP: {ip_address}")

    # Simulate a successful login
    if username == "admin" and password == "password":
        logging.info(f"Successful login: Username: {username}, IP: {ip_address}")
        return jsonify({"message": "Login successful!"}), 200
    else:
        logging.warning(f"Failed login attempt: Username: {username}, IP: {ip_address}")
        return jsonify({"message": "Login failed!"}), 401

if __name__ == '__main__':
    app.run(debug=True)