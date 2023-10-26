from fastapi import FastAPI
from pydantic import BaseModel
import redis


# Import ConversationBufferMemory
from langchain.memory import ConversationBufferMemory

# Define a request model for interacting with the agent
class AgentRequest(BaseModel):
    session_id: str
    query: str

# Initialize the FastAPI app
app = FastAPI()

# Initialize Redis connection
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Initialize the agent instance with ConversationBufferMemory
agent = initialize_agent(memory=ConversationBufferMemory())

# Define an API endpoint for interacting with the agent
@app.post("/agent")
def chat_with_agent(request: AgentRequest):
    session_id = request.session_id
    query = request.query

    # Retrieve the conversation history for the session_id from Redis
    conversation_history = redis_client.get(session_id)
    if conversation_history:
        conversation_history = conversation_history.decode('utf-8')
        conversation_history = eval(conversation_history)
    else:
        conversation_history = []

    # Use the agent instance to chat with the agent
    response = agent.run(query, conversation_history)

    # Update the conversation history for the session_id in Redis
    conversation_history.append(query)
    redis_client.set(session_id, str(conversation_history))

    return {"response": response}