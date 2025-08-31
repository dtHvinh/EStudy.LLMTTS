import asyncio
from fastapi import WebSocket
from typing import Dict, Optional


class WebSocketManager:
    def __init__(self):
        self.connections: Dict[str, WebSocket] = {}

    def add_connection(self, connection_id: str, connection: WebSocket):
        """Add a new WebSocket connection."""
        self.connections[connection_id] = connection

    def remove_connection(self, connection_id: str):
        """Remove a WebSocket connection."""
        if connection_id in self.connections:
            del self.connections[connection_id]

    def send_text(self, connection_id: str, message: str):
        """Send a message to a specific WebSocket connection."""
        if connection_id in self.connections:
            try:
                self.connections[connection_id].send_text(message)
            except Exception:
                # Connection is likely closed, remove it
                self.remove_connection(connection_id)

    def send_bytes(self, connection_id: str, message: bytes):
        """Send binary data to a specific WebSocket connection."""
        if connection_id in self.connections:
            try:
                self.connections[connection_id].send_bytes(message)
            except Exception:
                # Connection is likely closed, remove it
                self.remove_connection(connection_id)

    def broadcast_text(self, message: str):
        """Broadcast a message to all WebSocket connections."""
        closed_connections = []
        for connection_id, connection in self.connections.items():
            try:
                connection.send_text(message)
            except Exception:
                # Connection is closed, mark for removal
                closed_connections.append(connection_id)

        # Remove closed connections
        for connection_id in closed_connections:
            self.remove_connection(connection_id)

    def broadcast_bytes(self, message: bytes):
        """Broadcast binary data to all WebSocket connections."""
        closed_connections = []
        for connection_id, connection in self.connections.items():
            try:
                connection.send_bytes(message)
            except Exception:
                # Connection is closed, mark for removal
                closed_connections.append(connection_id)

        # Remove closed connections
        for connection_id in closed_connections:
            self.remove_connection(connection_id)

    async def close_connection(self, connection_id: str):
        """Close a specific WebSocket connection."""
        if connection_id in self.connections:
            try:
                # Check if connection is still open before trying to close
                connection = self.connections[connection_id]
                if (
                    hasattr(connection, "client_state") and connection.client_state == 1
                ):  # CONNECTED state
                    await connection.close()
            except Exception as e:
                # If closing fails (connection already closed), just log it
                pass
            finally:
                # Always remove from connections dict
                self.remove_connection(connection_id)


manager = WebSocketManager()
