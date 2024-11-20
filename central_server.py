import socket
import threading
import json
import heapq
from config import *

# Sample graph for station connectivity
graph_dict = {
    "Station 1": ["Station 3", "Station 4", "Station 8", "Station 9"],
    "Station 2": ["Station 7", "Station 9", "Station 6", "Station 8"],
    "Station 3": ["Station 1", "Station 8", "Station 4", "Station 5", "Station 7"],
    "Station 4": ["Station 1", "Station 3", "Station 7", "Station 8", "Station 9", "Station 6"],
    "Station 5": ["Station 3", "Station 6", "Station 8", "Station 10"],
    "Station 6": ["Station 5", "Station 2", "Station 4", "Station 8", "Station 10"],
    "Station 7": ["Station 2", "Station 4", "Station 3", "Station 8", "Station 9"],
    "Station 8": ["Station 3", "Station 4", "Station 5", "Station 6", "Station 7", "Station 1", "Station 2", "Station 9", "Station 10"],
    "Station 9": ["Station 2", "Station 4", "Station 1", "Station 7", "Station 8", "Station 10"],
    "Station 10": ["Station 5", "Station 9", "Station 6", "Station 8"]
}

class CentralServer:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(ADDR)
        # Initialize track_timers with tracks up to Track 30
        self.track_timers = {
            f"Track {i}": {"time": None, "station": None, "collision": False} for i in range(1, 31)
        }
        self.connected_clients = []

    def heuristic(self, station1, station2):
        # Simple heuristic for A*; in real scenarios, consider more sophisticated heuristics
        return 1

    def a_star_pathfinding(self, start, goal):
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {start: None}
        g_score = {node: float('inf') for node in graph_dict}
        g_score[start] = 0
        f_score = {node: float('inf') for node in graph_dict}
        f_score[start] = self.heuristic(start, goal)
        
        while open_set:
            _, current = heapq.heappop(open_set)
            if current == goal:
                path = []
                while current:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path
            
            for neighbor in graph_dict[current]:
                tentative_g_score = g_score[current] + 1
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                    if (f_score[neighbor], neighbor) not in open_set:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
        return None

    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")
        self.connected_clients.append(conn)
        connected = True
        while connected:
            try:
                msg_length = conn.recv(HEADER).decode(FORMAT)
                if msg_length:
                    msg_length = int(msg_length)
                    msg = conn.recv(msg_length).decode(FORMAT)
                    
                    if msg == DISCONNECT_MESSAGE:
                        connected = False
                        self.connected_clients.remove(conn)
                    else:
                        # Parse the message for station, track, and time
                        station = msg.split("|")[0]
                        track = msg.split("|")[1].split(" - ")[1]
                        time_remaining = int(msg.split("|")[2].split(" - ")[1].replace(" min", ""))
                        
                        print(f"[{station}] Using track {track} for {time_remaining} minutes")
                        
                        # Check if the track is clear
                        if not self.track_timers[track]["time"] or self.track_timers[track]["time"] <= 0:
                            self.track_timers[track]["time"] = time_remaining
                            self.track_timers[track]["station"] = station
                            self.track_timers[track]["collision"] = False
                            self.broadcast_status_update()
                            self.send_with_header(conn, f"Track {track} is clear for {time_remaining} minutes")
                        else:
                            # Collision detected, initiate A* pathfinding for alternate path
                            collision_msg = (f"COLLISION ALERT! Track {track} is already in use by "
                                            f"{self.track_timers[track]['station']} for next "
                                            f"{self.track_timers[track]['time']} minutes")
                            print(f"[COLLISION DETECTED] {collision_msg}")
                            self.track_timers[track]["collision"] = True
                            self.broadcast_status_update()
                            
                            # Attempt to find an alternate path from current station to destination
                            destination = "Station 10"  # Example destination; you may set this dynamically
                            new_path = self.a_star_pathfinding(station, destination)
                            if new_path:
                                path_msg = f"COLLISION: New path found: {' -> '.join(new_path)}"
                                print(f"[NEW PATH] {path_msg}")
                                self.send_with_header(conn, path_msg)
                            else:
                                no_path_msg = "COLLISION: No alternate path found."
                                print(f"[NO PATH AVAILABLE] {no_path_msg}")
                                self.send_with_header(conn, no_path_msg)
            except Exception as e:
                print(f"Error handling client {addr}: {e}")
                connected = False
                self.connected_clients.remove(conn)
        conn.close()


    def broadcast_status_update(self):
        status_update = json.dumps(self.track_timers)
        for client in self.connected_clients:
            try:
                self.send_with_header(client, status_update)
            except:
                client.close()
                self.connected_clients.remove(client)

    def send_with_header(self, conn, message):
        message = message.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        conn.send(send_length)
        conn.send(message)

    def start(self):
        self.server.listen()
        print(f"[LISTENING] Server is listening on {SERVER}")
        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
