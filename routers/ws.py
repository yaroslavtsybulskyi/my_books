from fastapi import WebSocket, WebSocketDisconnect, APIRouter

ws_router = APIRouter()


@ws_router.websocket("/ws/chat/{client_id}")
async def ws_chat(websocket: WebSocket, client_id: str) -> None:
    """
    WebSocket endpoint for a simple chat.
    :param websocket: The WebSocket connection instance.
    :param client_id: A unique client identifier passed in the URL.
    :return: None
    """
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Client {client_id} received {data}")
    except WebSocketDisconnect:
        print(f"Client {client_id} disconnected")
