from flask import Flask, session, request, jsonify
from flask_session import Session
import os

app = Flask(__name__)
# Check for environment variable for secret key or set a default one
app.secret_key = os.environ.get('SECRET_KEY', 'a_secret_key')

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
def home():
    return "Welcome to the Chatbot!"

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('input', '')
    if 'history' not in session:
        session['history'] = []
    session['history'].append(user_input)
    # Here you would normally handle the input and generate a response
    response = f"Received: {user_input}"
    return jsonify({'response': response, 'history': session['history']})

@app.route('/clear', methods=['POST'])
def clear_session():
    session.clear()
    return jsonify({'status': 'Session cleared'})

if __name__ == '__main__':
    app.run(debug=True)
