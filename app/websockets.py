import json
from uuid import UUID
from fastapi import WebSocket
from fastapi.encoders import jsonable_encoder

from app.models import WebsocketMessage


class Connection:
    """Represents a websocket connection."""

    def __init__(self, websocket: WebSocket, id: UUID):
        self.websocket: WebSocket = websocket
        self.id: UUID = id


class Connections:
    """Manages active connections."""

    def __init__(self):
        self.active_connections: dict[UUID, Connection] = {}
        # self.active_unauthenticated_connections: dict[UUID, Connection] = {}

    def connect(self, websocket: WebSocket, id: UUID) -> None:
        """
        Connects a websocket.
        Args:
            websocket: The websocket to connect.
            id: The id of the connection.
        """

        self.active_connections[id] = Connection(websocket, id)

    def disconnect(self, id: UUID) -> None:
        """
        Disconnects a websocket.
        Args:
            id: The id of the connection.
        """

        self.active_connections.pop(id)

    async def send(self, id: UUID, message: WebsocketMessage) -> None:
        """
        Sends a message to a websocket.
        Args:
            id: The id of the connection.
            message: The message to send.
        """

        json_compatible_message = jsonable_encoder(message)
        json_message = json.dumps(json_compatible_message)
        await self.active_connections[id].websocket.send_text(json_message)

    async def broadcast(self, message: WebsocketMessage) -> None:
        """
        Broadcasts a message to all active connections.
        Args:
            message: The message to broadcast.
        """

        json_compatible_message = jsonable_encoder(message)
        json_message = json.dumps(json_compatible_message)
        for connection in self.active_connections.values():
            await connection.websocket.send_text(json_message)

    def get_number_of_connections(self) -> int:
        """
        Gets the number of active connections.

        The current websocket session is not counted.
        Returns:
            The number of active connections.
        """

        return len(self.active_connections)
