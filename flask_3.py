from flask import Flask, session, request, jsonify
from flask_session import Session
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'a_secret_key')

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
def home():
    return "Welcome to the Chatbot! Please use the /start endpoint to begin and set your name."

@app.route('/start', methods=['POST'])
def start_session():
    name = request.json.get('name', '')
    if name == '':
        return jsonify({'error': 'Name is required'}), 400
    if 'users' not in session:
        session['users'] = {}
    if name not in session['users']:
        session['users'][name] = []
    return jsonify({'message': f'Session started for {name}'}), 200

@app.route('/chat', methods=['POST'])
def chat():
    name = request.json.get('name', '')
    user_input = request.json.get('input', '')
    if name == '' or user_input == '':
        return jsonify({'error': 'Name and input are required'}), 400
    if 'users' in session and name in session['users']:
        session['users'][name].append(user_input)
        # Normally you would process the input here to generate a response
        response = f"Received: {user_input}"
        return jsonify({'response': response, 'history': session['users'][name]})
    else:
        return jsonify({'error': 'Session not started or invalid name'}), 404

@app.route('/clear', methods=['POST'])
def clear_session():
    name = request.json.get('name', '')
    if name == '':
        return jsonify({'error': 'Name is required to clear session'}), 400
    if 'users' in session and name in session['users']:
        del session['users'][name]
        return jsonify({'status': f'Session cleared for {name}'})
    else:
        return jsonify({'error': 'No session found for this name'}), 404

if __name__ == '__main__':
    app.run(debug=True)
