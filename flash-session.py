from flask import Flask, session, request, redirect, url_for

app = Flask(__name__)

# Secret key for session management. Use a strong, random value in production.
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    # Display stored data or a message if nothing is stored
    data = session.get('info', 'No data stored.')
    return f"Stored data: {data}<br><a href='/input'>Input Data</a> | <a href='/clear'>Clear Data</a>"

@app.route('/input', methods=['GET', 'POST'])
def input_data():
    if request.method == 'POST':
        # Store the data in the session dictionary
        session['info'] = request.form['data']
        return redirect(url_for('index'))
    return '''
        <form method="post">
            Data: <input type="text" name="data"><br>
            <input type="submit" value="Submit">
        </form>
    '''

@app.route('/clear')
def clear_data():
    # Clear the session dictionary
    session.pop('info', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
