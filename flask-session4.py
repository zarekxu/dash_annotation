from flask import Flask, session, request, jsonify, render_template_string
from flask_session import Session
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'a_secret_key')

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# HTML template for the home and start session form
HOME_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chatbot Session Starter</title>
</head>
<body>
    <h1>Welcome to the Chatbot!</h1>
    <form action="/start" method="post">
        <label for="name">Enter your name to start a session:</label>
        <input type="text" id="name" name="name" required>
        <button type="submit">Start Session</button>
    </form>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HOME_TEMPLATE)

@app.route('/start', methods=['GET', 'POST'])
def start_session():
    if request.method == 'POST':
        name = request.form.get('name', '')
        if name == '':
            return 'Name is required', 400
        if 'users' not in session:
            session['users'] = {}
        if name not in session['users']:
            session['users'][name] = []
        return f'Session started for {name}. You can now use the /chat endpoint to communicate.'
    return render_template_string(HOME_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    name = request.json.get('name', '')
    user_input = request.json.get('input', '')
    if name == '' or user_input == '':
        return jsonify({'error': 'Name and input are required'}), 400
    if 'users' in session and name in session['users']:
        session['users'][name].append(user_input)
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
