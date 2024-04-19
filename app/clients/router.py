from uuid import UUID
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.pixelcode import PixelCode
from app.clients.models import (
    WebsocketMessage,
)
from app.clients.utils import Connections
from app.clients.services import (
    on_client_connect,
    on_client_disconnect,
    validate_message,
)

router = APIRouter(
    prefix="/ws",
    tags=["ws"],
)

client_connections: Connections = Connections()
pixel_code: PixelCode = PixelCode()


@router.websocket("/client")
async def client_endpoint(websocket: WebSocket, client_id: UUID):
    await websocket.accept()  # Accept the websocket connection

    try:
        await on_client_connect(client_connections, websocket, client_id)

        while True:
            message: WebsocketMessage | None = await validate_message(
                websocket, client_id, client_connections
            )
            if message is None:
                continue
            else:
                action: str = message.action

                if action == "employee_info":
                    pass
                if action == "email_verification":
                    pass
    except WebSocketDisconnect:
        await on_client_disconnect(client_connections, websocket, client_id)
