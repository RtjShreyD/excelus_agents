from fastapi import FastAPI, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from lib.agent import MedicalReceptionAgent
from core.dependencies import validate_token
from core.validators import InitializationRequest, ChatRequest, MessageRequest
import uuid
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from lib.info_handler import InfoHandler
from workers.operations import ask_agent
# import logging

# log = logging.getLogger(__name__)

app = FastAPI()
agent_instance = MedicalReceptionAgent()
info_handler = InfoHandler()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # Set this to the appropriate origins in your production environment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/initialise")
async def initialize_resources(
    request_body: InitializationRequest, token: str = Depends(validate_token)
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
    request_body: ChatRequest, token: str = Depends(validate_token)
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



@app.post("/process_query")
async def chat_functionality(
    request_body: MessageRequest, token: str = Depends(validate_token)
):
    """
    Process a chat query and initiate a Celery task.

    - **session_id**: Unique identifier for the session.
    - **query**: The chat query to be processed.

    Returns:
    - **status**: HTTP status code.
    - **msg**: Message indicating success or failure.
    - **details**: Additional details, including session_id and task_id.
    """
    try:
        print("Started")
        session_id = request_body.session_id
        query = request_body.query

        print(session_id, query)

        if not session_id:
            print("Session ID not specified - Aborting...")
            response = {
                "status": 400,
                "msg": "Failure - Session ID not specified - Aborting...",
                "details": {},
            }
            return jsonable_encoder(response)
        
        else:
            is_registered = info_handler.is_registered_session(session_id)
            if not is_registered:
                print("Session ID not registered - Aborting...")
                response = {
                    "status": 401,
                    "msg": "Failure - Session ID not registered - Aborting...",
                    "details": {},
                }
                return jsonable_encoder(response)
            
            else:
                print("Is registered")
                input_obj = {
                    'session_id': session_id,
                    'query' : query,
                }
                task = ask_agent.apply_async(args=[input_obj], countdown=0)

                response = {
                    "status": 200,
                    "msg": "Success",
                    "details": {"session_id": session_id, "task_id": task.id}
                }
                print(task)

                return jsonable_encoder(response)

    except Exception as e:
        print(f"Exception - {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/check_reponse/{session_id}/{task_id}")
async def check_task(session_id: str, task_id: str, token: str = Depends(validate_token)):
    """
    Check the response of a Celery task.

    - **session_id**: Unique identifier for the session.
    - **task_id**: Unique identifier for the Celery task.

    Returns:
    - **status**: HTTP status code.
    - **msg**: Message indicating success or failure.
    - **details**: Additional details, including session_id, task_id, and agent_response.
    """
    try:
        agent_resp = info_handler.check_response(task_id)
        response = {
                    "status": 200,
                    "msg": "Success",
                    "details": {"session_id": session_id, "task_id": task_id, "agent_response": agent_resp},
                }
        
        return jsonable_encoder(response)

    except Exception as e:
        print(f"Exception - {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
