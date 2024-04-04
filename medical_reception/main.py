from fastapi import FastAPI, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from lib.agent import MedicalReceptionAgent
from core.dependencies import validate_token
from core.validators import InitializationRequest, ChatRequest, MessageRequest
import uuid
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from lib.info_handler import InfoHandler

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


@app.post("/initialise")
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


@app.post("/chat")
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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)