from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# In-memory storage for user state
user_states = {}

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_id = data.get('user_id')
    message = data.get('message')

    if user_id not in user_states:
        user_states[user_id] = {"step": "ask_name"}

    current_step = user_states[user_id]["step"]

    if current_step == "ask_name":
        user_states[user_id] = {"step": "ask_age", "name": message}
        return jsonify({"message": f"Nice to meet you, {message}! How old are you?"})

    if current_step == "ask_age":
        # Here you could add validation for the age if necessary
        user_states[user_id]["step"] = "ask_resource"
        user_states[user_id]["age"] = message  # Store the age, even though we don't use it further in this example
        return jsonify({"message": "What resource are you looking for?"})

    if current_step == "ask_resource":
        resource_name = message
        # Logic to fetch or interact with the requested resource can be added here.
        return jsonify({"message": f"Thank you. You asked for resource: {resource_name}. How can I assist you further?"})

    return jsonify({"message": "How can I assist you?"})

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
