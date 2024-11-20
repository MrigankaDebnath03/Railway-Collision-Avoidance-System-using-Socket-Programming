# app.py

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import socket
import json
from config import *

app = Flask(__name__)
socketio = SocketIO(app)

# Generating track and station data
stations = [f"S{i}" for i in range(1, 11)]  # 10 stations: S1 to S10
tracks = [f"Track {i}" for i in range(1, 53)]  # 52 tracks: Track 1 to Track 52

# Initialize track status
track_status = {track: {"time": 0, "station": None, "collision": False} for track in tracks}

@app.route('/')
def index():
    return render_template('index.html', stations=stations, tracks=tracks)

@socketio.on('connect')
def handle_connect():
    # Send the initial track status when a client connects
    emit('track_status_update', track_status)

# Function to update the track status and handle changes
def update_track_status():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect(ADDR)

    while True:
        try:
            msg_length = server_socket.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = server_socket.recv(msg_length).decode(FORMAT)
                
                status_update = json.loads(msg)
                for track, status in status_update.items():
                    track_status[track] = status
                
                # Broadcast the updated status to all connected clients
                socketio.emit('track_status_update', track_status)
        except Exception as e:
            print(f"Error updating track status: {e}")
            break

socketio.start_background_task(target=update_track_status)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
