from flask import Flask, render_template, request, jsonify, redirect, url_for
import pyrebase
from dashboard import generate_dashboard


# Firebase configuration
config = {
  'apiKey': "AIzaSyBoF9TYrU6Vvh9xxkpP7Omn_e1kYsDSVgI",
  'authDomain': "first-aa0d4.firebaseapp.com",
  'databaseURL': "https://first-aa0d4-default-rtdb.firebaseio.com",
  'projectId': "first-aa0d4",
  'storageBucket': "first-aa0d4.appspot.com",
  'messagingSenderId': "98927499335",
  'appId': "1:98927499335:web:642ed7333d04ed88477962"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

app = Flask(__name__, static_folder='assets', template_folder='templates')

@app.route('/')
def index():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    password = request.form['password']
    
    try:
        user = auth.create_user_with_email_and_password(email, password)
        return jsonify({'success': True, 'message': 'User created successfully!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form['email']
    password = request.form['password']
    
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        return redirect(url_for('dashboard', user_email=email))
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/dashboard')
def dashboard():
    user_email = request.args.get('user_email')
    if user_email:
        # Call generate_dashboard function to generate dashboard content
        dashboard_content = generate_dashboard(user_email)
        return dashboard_content
    else:
        return redirect(url_for('login'))

@app.route('/logout', methods=['POST'])
def logout():
    # Log user out
    auth.current_user = None
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)
