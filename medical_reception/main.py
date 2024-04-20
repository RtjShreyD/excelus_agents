from fastapi import FastAPI, Depends, HTTPException, WebSocket
from fastapi.encoders import jsonable_encoder
from lib.agent import MedicalReceptionAgent
from core.dependencies import validate_token
from core.validators import InitializationRequest, ChatRequest, MessageRequest
import uuid
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from lib.info_handler import InfoHandler
from starlette.websockets import WebSocketDisconnect

app = FastAPI()
agent_instance = MedicalReceptionAgent()
info_handler = InfoHandler()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

active_sessions = {}


@app.post("/api/v1/initialise")
async def initialize_resources(
    request_body: InitializationRequest
):
    """
    Initialize resources.

    This endpoint initializes resources.

    Args:
        request_body (InitializationRequest): JSON request body containing session_id.

    Returns:
        dict: Response dictionary.
    """
    try:
        session_id = request_body.session_id

        if not session_id:
            session_id = str(uuid.uuid4())[:6]
        else:
            session_id = request_body.session_id

        agent_response = agent_instance.agent_begin(session_id)

        response = {
            "status": 201,
            "msg": "Initialized",
            "details": {"session_id": session_id, "agent_response": agent_response},
        }

        return jsonable_encoder(response)

    except Exception as e:
        print(f"Exception - {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.post("/api/v1/chat")
async def chat_functionality(
    request_body: ChatRequest
):
    """
    Implement chat functionality.

    This endpoint implements chat functionality.

    Args:
        request_body (ChatRequest): JSON request body containing session_id and human_message.

    Returns:
        dict: Response dictionary.
    """
    try:
        # Extract session_id and human_message from the request body
        session_id = request_body.session_id
        human_message = request_body.human_message

        if not session_id.strip():
            raise HTTPException(status_code=400, detail="session_id cannot be empty")

        if not human_message.strip():
            raise HTTPException(status_code=400, detail="human_message cannot be empty")

        # Mocking agent response
        agent_response = agent_instance.agent_chat(session_id, human_message)

        # Response format
        response = {
            "status": 200,
            "msg": "Success",
            "details": {"session_id": session_id, "agent_response": agent_response},
        }

        return jsonable_encoder(response)

    except Exception as e:
        print(f"Exception - {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")



@app.websocket("/api/v2/ws_chat/{session_id}")
async def chat_ws_endpoint(session_id: str, websocket: WebSocket):
    """
    WebSocket endpoint for chat.

    Args:
        session_id (str): Session ID for the chat session.
        websocket (WebSocket): WebSocket connection object.

    Returns:
        None
    """
    try:
        # Accept the WebSocket connection
        await websocket.accept()

        # If session_id is not provided by the client, generate one
        if session_id is None:
            session_id = str(uuid.uuid4())[:6]

        # Initialize the agent and send the initial response
        async for chunk in agent_instance.agent_begin_stream(session_id):
            await websocket.send_text(chunk)

        await websocket.send_text('@$') # Sending the @$ character after initial agent response denotes response is completed

        # Store the WebSocket connection in active connections dictionary
        if session_id not in active_sessions:
            active_sessions[session_id] = set()
        active_sessions[session_id].add(websocket)


        # Exchange messages
        while True:
            message = await websocket.receive_text()
            # Query the chatbot and send the response back in chunks
            async for chunk in agent_instance.agent_chat_stream(session_id, message):
                await websocket.send_text(chunk)
            
            await websocket.send_text('@$')

    except WebSocketDisconnect as wsd:
        print(f"WebSocketDisconnect: {wsd.code}")
        # Remove the WebSocket connection from active sessions if an error occurs
        if session_id in active_sessions:
            active_sessions[session_id].remove(websocket)
        await websocket.close(code=1000)  # Close WebSocket connection cleanly

    except Exception as e:
        print(f"Exception - {str(e)}")
        # Remove the WebSocket connection from active sessions if an error occurs
        if session_id in active_sessions:
            active_sessions[session_id].remove(websocket)
        await websocket.close(code=1011)  # Close WebSocket connection with error status code
    
    finally:
        # Close the session if no more clients are connected
        if session_id in active_sessions and len(active_sessions[session_id]) == 0:
            active_sessions.pop(session_id, None)





if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)