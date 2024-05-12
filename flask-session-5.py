from flask import Flask, session, request, jsonify, render_template_string
from flask_session import Session
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'a_secret_key')

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# HTML template for the home, start, and clear session form
HOME_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chatbot Session Management</title>
</head>
<body>
    <h1>Welcome to the Chatbot!</h1>
    <form action="/start" method="post">
        <label for="name">Enter your name to start a session:</label>
        <input type="text" id="name" name="name" required>
        <button type="submit">Start Session</button>
    </form>
    <hr>
    <form action="/clear" method="post">
        <label for="clearname">Enter your name to clear your session:</label>
        <input type="text" id="clearname" name="name" required>
        <button type="submit">Clear Session</button>
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

@app.route('/clear', methods=['GET', 'POST'])
def clear_session():
    if request.method == 'POST':
        name = request.form.get('name', '')
        if name == '':
            return 'Name is required to clear session', 400
        if 'users' in session and name in session['users']:
            del session['users'][name]
            return f'Session cleared for {name}'
        else:
            return 'No session found for this name', 404
    return render_template_string(HOME_TEMPLATE)

if __name__ == '__main__':
    app.run(debug=True)
