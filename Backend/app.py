# Flask & extensions
from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# External libraries
import bcrypt
import jwt

# Built-in libraries
import datetime
import re
import requests
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'this_is_a_very_secure_secret_key_12345'
CORS(app, supports_credentials=True)
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)   

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    role = db.Column(db.String(50), default="user")
    failed_attempts = db.Column(db.Integer, default=0)
    is_locked = db.Column(db.Boolean, default=False)

def check_role(required_role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = request.headers.get("Authorization")

            if not token:
                return jsonify({"error": "Token missing"}), 401

            try:
                token = token.split(" ")[1]
                decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])

                if decoded.get("role") != required_role:
                    return jsonify({"error": "Access denied"}), 403

                request.user = decoded
            except:
                return jsonify({"error": "Invalid token"}), 401

            return func(*args, **kwargs)
        return wrapper
    return decorator

@app.route('/register', methods=['POST'])
def register():
    print("API HIT")
    try:
        data = request.get_json()

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        # Check empty
        if not username or not email or not password:
            return jsonify({"error": "Missing fields"}), 400

        # Check email format
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, email):
            return jsonify({"error": "Invalid email"}), 400

        # Check password length
        if len(password) < 6:
            return jsonify({"error": "Password must be at least 6 characters"}), 400

        # hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        role = data.get('role', 'user')
        
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"error": "User already exists"}), 400

        new_user = User(
            username=username,
            email=email,
            password=hashed_password.decode('utf-8'),
            role=role
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User registered successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/login', methods=['POST'])
def login():
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')
        captcha_response = data.get("captcha")

        if not captcha_response:
            return jsonify({"error": "CAPTCHA required"}), 400

        secret_key = "6LevHJgsAAAAADqf1GzvQnP0gnwfQcWMtmWM3azT"

        verify_url = "https://www.google.com/recaptcha/api/siteverify"

        response = requests.post(verify_url, data={
            "secret": secret_key,
            "response": captcha_response
        })

        result = response.json()

        if not result.get("success"):
            return jsonify({"error": "CAPTCHA failed"}), 400
        user = User.query.filter_by(email=email).first()
        if user and user.is_locked:
            return jsonify({"error": "Account is locked"}), 403

        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Wrong password
        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):

            user.failed_attempts += 1

            if user.failed_attempts >= 3:
                user.is_locked = True

            db.session.commit()

            return jsonify({"error": "Invalid password"}), 401
        # SUCCESS LOGIN
        user.failed_attempts = 0
        db.session.commit()

        # THEN generate token
        token = jwt.encode({
            'user_id': user.id,
            'email': user.email,
            'role': user.role,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({
            "message": "Login successful",
            "token": token
        }), 200
@app.route('/dashboard', methods=['GET'])
def dashboard():
    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"error": "Token missing"}), 401
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return jsonify({"error": "Token missing"}), 401

    try:
        token = auth_header.split(" ")[1]
    except:
        return jsonify({"error": "Invalid token format"}), 401

    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return jsonify({"message": f"Welcome {data['email']}"}), 200

    except:
        return jsonify({"error": "Invalid or expired token"}), 401

@app.route('/')
def home():
    return "Backend Running 🚀"

@app.route('/admin', methods=['GET'])
@check_role("admin")
def admin_route():
    return jsonify({"message": "Welcome Admin"})

@app.route('/users', methods=['GET'])
@check_role("admin")
def get_users():
    users = User.query.all()

    user_list = []
    for user in users:
        user_list.append({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        })

    return jsonify(user_list)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)