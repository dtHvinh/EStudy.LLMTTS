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
            self.connections[connection_id].send_text(message)

    def send_bytes(self, connection_id: str, message: bytes):
        """Send binary data to a specific WebSocket connection."""
        if connection_id in self.connections:
            self.connections[connection_id].send_bytes(message)

    def broadcast_text(self, message: str):
        """Broadcast a message to all WebSocket connections."""
        for connection in self.connections.values():
            connection.send_text(message)

    def broadcast_bytes(self, message: bytes):
        """Broadcast binary data to all WebSocket connections."""
        for connection in self.connections.values():
            connection.send_bytes(message)

    async def close_connection(self, connection_id: str):
        """Close a specific WebSocket connection."""
        if connection_id in self.connections:
            await self.connections[connection_id].close()
            self.remove_connection(connection_id)


manager = WebSocketManager()
