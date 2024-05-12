from flask import Flask, session, request, jsonify, render_template_string, redirect, url_for
from flask_session import Session
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'a_secret_key')

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# HTML template for the home page and chat page
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
        <label for="name">Enter your name:</label>
        <input type="text" id="name" name="name" required>
        <button type="submit">Start Chatting</button>
    </form>
</body>
</html>
"""

CHAT_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chat Page</title>
</head>
<body>
    <h1>Chat with Our Bot</h1>
    <form action="/chat" method="post">
        <input type="hidden" name="name" value="{{ name }}">
        <label for="message">Your Message:</label>
        <input type="text" id="message" name="message" required>
        <button type="submit">Send</button>
    </form>
    <hr>
    <button onclick="window.location.href='/clear?name={{ name }}'">Clear Session</button>
    {% if history %}
        <h2>Chat History</h2>
        <ul>
            {% for msg in history %}
                <li>{{ msg }}</li>
            {% end %}
        </ul>
    {% endif %}
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HOME_TEMPLATE)

@app.route('/start', methods=['POST'])
def start_session():
    name = request.form['name']
    if 'users' not in session:
        session['users'] = {}
    if name not in session['users']:
        session['users'][name] = []
    return render_template_string(CHAT_TEMPLATE, name=name, history=session['users'][name])

@app.route('/chat', methods=['POST'])
def chat():
    name = request.form['name']
    message = request.form['message']
    if name and message:
        if 'users' in session and name in session['users']:
            session['users'][name].append(message)
            history = session['users'][name]
        else:
            return redirect(url_for('home'))
        return render_template_string(CHAT_TEMPLATE, name=name, history=history)
    else:
        return redirect(url_for('home'))

@app.route('/clear')
def clear_session():
    name = request.args.get('name', '')
    if name and 'users' in session and name in session['users']:
        del session['users'][name]
        return redirect(url_for('home'))
    else:
        return 'Session not found or name not provided', 404

if __name__ == '__main__':
    app.run(debug=True)
