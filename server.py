import pickle
import os
from flask import Flask, send_from_directory
from flask_socketio import SocketIO
from flask_cors import CORS
from pythonosc import osc_message_builder
from pythonosc.udp_client import SimpleUDPClient

# Load the trained ML model from the correct path
model_path = os.path.join('ml', 'model.pkl')
with open(model_path, 'rb') as model_file:
    model = pickle.load(model_file)

# Initialize Flask app and configure SocketIO
app = Flask(__name__, static_folder='public')
socketio = SocketIO(app)
CORS(app, resources={r"/*": {"origins": ["http://localhost:8000", "http://127.0.0.1:8000"]}})
osc_client = SimpleUDPClient('127.0.0.1', 57120)

@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

@socketio.on('message')
def handle_message(message):
    print(f"Received message: {message}")

    prediction = model.predict([message])[0]
    if prediction == 1:
        print("⚠️ Troll message detected! Sending OSC trigger.")
        osc_message = osc_message_builder.OscMessageBuilder(address="/trigger")
        osc_message.add_arg(1)
        osc_client.send(osc_message.build())

if __name__ == '__main__':
    print("Starting the server on http://127.0.0.1:8000...")
    socketio.run(app, host='0.0.0.0', port=8000)
