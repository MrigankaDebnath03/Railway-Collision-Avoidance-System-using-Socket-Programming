import socket
from config import *

class RailwayStation:
    def __init__(self, name, connected_tracks):
        self.name = name
        self.connected_tracks = connected_tracks
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(ADDR)

    def send_train(self, track, time):
        if track not in self.connected_tracks:
            print(f"Error: Station {self.name} is not connected to track {track}")
            return
            
        message = f"{self.name}|Track - {track}|Time - {time} min"
        self._send(message)
        response = self._receive()
        print(f"[SERVER RESPONSE to {self.name}] {response}")

    def _send(self, msg):
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)

    def _receive(self):
        try:
            msg_length = self.client.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                return self.client.recv(msg_length).decode(FORMAT)
        except ValueError:
            print("Error: Received an incorrectly formatted message")
            return ""
        return ""

    def disconnect(self):
        self._send(DISCONNECT_MESSAGE)
        self.client.close()
