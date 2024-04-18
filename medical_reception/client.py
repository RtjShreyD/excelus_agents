import asyncio
import uuid
import websockets
import time

async def chat_client():
    session_id = str(uuid.uuid4())
    uri = f"ws://localhost:8001/api/v2/ws_chat/{session_id}"  # Replace with your WebSocket server URI

    async with websockets.connect(uri) as websocket:
        # Receive and print all initial messages from the server
        while True:
            response = await websocket.recv()
            if response == "@$":
                print('\n -------------------------------- \n')
                break
            else:
                print(response, end = ' ')
        
        message = "I need to visit a General Physician"
        await websocket.send(message)

        while True:
            response = await websocket.recv()
            if response == "@$":
                break
            else:
                print(response, end = ' ')


asyncio.run(chat_client())
