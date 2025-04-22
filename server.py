from flask import Flask, send_from_directory
from flask_socketio import SocketIO
from flask_cors import CORS
from pythonosc import osc_message_builder
from pythonosc.udp_client import SimpleUDPClient

# Initialize Flask app and configure SocketIO
app = Flask(__name__, static_folder='public')
socketio = SocketIO(app)

# Enable CORS for specific origins
CORS(app, resources={r"/*": {"origins": ["http://localhost:8000", "http://127.0.0.1:8000"]}})

# Initialize OSC client for sending messages to SuperCollider
osc_client = SimpleUDPClient('127.0.0.1', 57120)

# A simple route to serve the main HTML page
@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

# SocketIO event for chat messages
@socketio.on('message')
def handle_message(message):
    print(f"Received message: {message}")
    
    # List of troll keywords to trigger OSC messages
    troll_keywords = ['spam', 'troll', 'hack', 'idiot', 'cry', 'snowflake']
    
    # Check if any troll keyword is in the received message
    if any(keyword in message.lower() for keyword in troll_keywords):
        print(f"Troll keyword detected: {message}")
        
        # Send OSC message to SuperCollider when troll message is detected
        osc_message = osc_message_builder.OscMessageBuilder(address="/trigger")  # Updated trigger address
        osc_message.add_arg(1)  # Example argument
        osc_message = osc_message.build()
        
        # Send OSC message to SuperCollider
        osc_client.send(osc_message)
        
        # Emit a 'glitch' event to the front-end to trigger the glitch effect
        socketio.emit('glitch', {'message': message})

# Start the server with SocketIO
if __name__ == '__main__':
    print("Starting the server on http://127.0.0.1:8000...")
    socketio.run(app, host='0.0.0.0', port=8000)
    print("Server successfully running!")
