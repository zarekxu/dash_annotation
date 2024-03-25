from flask import Flask, request, jsonify

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

    if user_states[user_id]["step"] == "ask_name":
        user_states[user_id] = {"step": "ask_resource", "name": message}
        return jsonify({"message": f"Hi {message}, what resource are you looking for?"})
    elif user_states[user_id]["step"] == "ask_resource":
        resource_name = message
        # Here you could add logic to fetch or interact with the requested resource.
        return jsonify({"message": f"Thank you. You asked for resource: {resource_name}. How can I assist you further?"})

    return jsonify({"message": "How can I assist you?"})

if __name__ == '__main__':
    app.run(debug=True)
