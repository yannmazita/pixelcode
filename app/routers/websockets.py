from uuid import UUID
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import ValidationError
from app.models import (
    AppStats,
    AppError,
    WebsocketMessage,
)
from app.websockets import Connections

router = APIRouter(
    prefix="/ws",
    tags=["ws"],
)

client_connections: Connections = Connections()


async def verify_websocket_token(websocket: WebSocket) -> None:
    """
    Verifies the websocket token.
    The websocket token is the first message sent by the user.
    It contains the access token and token type. This function verifies
    the token and closes the websocket if it is invalint
    Args:
        websocket: The websocket to verify.
    """

    try:
        # do things to actually verify the token
        pass
    except ValidationError:
        await websocket.close()
        print("Invalid token format.")


async def on_client_connect(websocket: WebSocket, client_id: UUID) -> None:
    """
    Handles actions when a websocket is connected.
    Args:
        websocket: The websocket to connect.
        client_id: The id of the client.
    """
    client_connections.connect(websocket, client_id)
    stats = AppStats(active_users=client_connections.get_number_of_connections())
    stats_message = WebsocketMessage(action="server_stats", data=stats)
    await client_connections.broadcast(stats_message)


async def on_client_disconnect(websocket: WebSocket, client_id: UUID) -> None:
    """
    Handles actions when a websocket is disconnected.
    Args:
        websocket: The websocket to disconnect.
        client_id: The id of the client.
    """
    client_connections.disconnect(client_id)
    stats = AppStats(active_users=client_connections.get_number_of_connections())
    stats_message = WebsocketMessage(action="server_stats", data=stats)
    await client_connections.broadcast(stats_message)


async def validate_message(
    websocket: WebSocket, id: UUID, connections: Connections
) -> WebsocketMessage | None:
    """
    Validates a message received from the websocket.
    This function receives a message from the websocket, validates it,
    and sends back an error message if the message is invalid.
    Args:
        websocket: The websocket to receive the message from.
        id: The id of the websocket connection.
        connections: The object that holds the websocket connections.
    """
    raw_message: str = await websocket.receive_text()
    try:
        message: WebsocketMessage = WebsocketMessage.model_validate_json(raw_message)
        return message
    except ValidationError as e:
        error: AppError = AppError(error=str(e))
        error_message = WebsocketMessage(action="error", data=error)
        await connections.send(id, error_message)
        return None


@router.websocket("/client")
async def client_endpoint(websocket: WebSocket, client_id: UUID):
    await websocket.accept()  # Accept the websocket connection

    try:
        await on_client_connect(websocket, client_id)

        while True:
            message: WebsocketMessage | None = await validate_message(
                websocket, client_id, client_connections
            )
            if message is None:
                continue
            else:
                action: str = message.action

                if action == "server_stats":
                    stats: AppStats = AppStats(
                        active_users=client_connections.get_number_of_connections()
                    )
                    stats_message: WebsocketMessage = WebsocketMessage(
                        action="server_stats", data=stats
                    )
                    await client_connections.send(client_id, stats_message)

    except WebSocketDisconnect:
        await on_client_disconnect(websocket, client_id)
