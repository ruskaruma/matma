from fastapi import WebSocket, WebSocketDisconnect

async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            text=await websocket.receive_text()
            await websocket.send_json({
                "query": text,
                "results": ["streamed_stub1","streamed_stub2"]
            })
    except WebSocketDisconnect:
        print("Client disconnected.")