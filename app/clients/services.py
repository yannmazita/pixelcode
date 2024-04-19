from uuid import UUID
from fastapi import WebSocket
from pydantic import ValidationError
from app.clients.utils import Connections
from app.clients.models import (
    AppStats,
    AppError,
    WebsocketMessage,
)


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


async def on_client_connect(
    client_connections: Connections, websocket: WebSocket, client_id: UUID
) -> None:
    """
    Handles actions when a websocket is connected.
    Args:
        client_connections: The object that holds the websocket connections.
        websocket: The websocket to connect.
        client_id: The id of the client.
    """
    client_connections.connect(websocket, client_id)
    stats = AppStats(active_users=client_connections.get_number_of_connections())
    stats_message = WebsocketMessage(action="server_stats", data=stats)
    await client_connections.broadcast(stats_message)


async def on_client_disconnect(
    client_connections: Connections, websocket: WebSocket, client_id: UUID
) -> None:
    """
    Handles actions when a websocket is disconnected.
    Args:
        client_connections: The object that holds the websocket connections.
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


async def process_employee_info(
    client_connections: Connections, client_id: UUID, message: WebsocketMessage
) -> None:
    """
    Processes the employee information.
    This function processes the employee information and sends it back to the client.
    Args:
        client_connections: The object that holds the websocket connections.
        client_id: The id of the client.
        message: The message containing the employee information.
    """
    try:
        pass
    except ValidationError as e:
        error: AppError = AppError(error=str(e))
        error_message = WebsocketMessage(action="error", data=error)
        await client_connections.send(client_id, error_message)


async def verify_email_code(
    client_connections: Connections, client_id: UUID, message: WebsocketMessage
) -> None:
    """
    Verifies the email code.
    This function verifies the email code sent by the client.
    Args:
        client_connections: The object that holds the websocket connections.
        client_id: The id of the client.
        message: The message containing the email code.
    """
    try:
        pass
    except ValidationError as e:
        error: AppError = AppError(error=str(e))
        error_message = WebsocketMessage(action="error", data=error)
        await client_connections.send(client_id, error_message)
