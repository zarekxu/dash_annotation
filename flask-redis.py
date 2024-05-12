from flask import Flask, session
from flask_session import Session

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REDIS'] = redis.from_url('redis://localhost:6379')

Session(app)

@app.route('/set_object', methods=['POST'])
def set_object():
    my_object = SomeComplexClass('John', 30)
    session['my_object'] = my_object  # Directly store objects
    return 'Object set in session'

@app.route('/get_object')
def get_object():
    my_object = session.get('my_object', None)
    return f'Object retrieved: {my_object.name}'
