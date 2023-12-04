from celery import Celery
import logging
import os
import time
from dotenv import load_dotenv
from lib.agent import MedicalReceptionAgent
from lib.info_handler import InfoHandler

load_dotenv()

log = logging.getLogger(__name__)

app = Celery(__name__)
app.conf.broker_url = os.environ.get("CELERY_BROKER_URL")
app.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND")
app.conf.broker_connection_retry = True
app.conf.acks_late=True

agent_instance = MedicalReceptionAgent()
info_handler = InfoHandler()

'''
input = {
    'session_id': "",
    'call_sid': "",
    'query' : ""
}

'''

@app.task
def operator(inputs):
    try:
        session_id = inputs.get("session_id")
        log.info("Operating - " + session_id)
        time.sleep(30)
        log.info("Operation completed successfully")
        return True
    
    except Exception as e:
        log.error("Error executing operation - " + str(e))
        return False


# This considers agent has already been initialized for a session_id
# if session_id is not passed in inputs, this should fail
# if session_id is not registered in Redis, this should fail
# if session_id is registered in Redis, pass it to the agent
# once agent response is available, store the response in Celery Result backend.
@app.task
def ask_agent(inputs):
    try:
        log.info("Ask agent Activated...")

        session_id = inputs.get("session_id")
        call_sid = inputs.get("call_sid", "")
        query = inputs.get("query")

        if not session_id:
            log.warning("Session ID not specified - Aborting...")
            result = {
                'status': False,
                'session_id': "",
                'msg' : "Session ID not specified - Aborting...",
                'agent_resp' : ""
            }
            return result
        
        is_registered = info_handler.is_registered_session(session_id)
        if not is_registered:
            log.warning("Session ID not registered - Aborting...")
            result = {
                'status': False,
                'error' : False,
                'session_id': "",
                'msg' : "Session ID not registered - Aborting...",
                'agent_resp' : ""
            }
            return result

        log.info("Operating - " + session_id)
        log.info("Query - " + query)

        agent_response = agent_instance.agent_chat(session_id, query)
        result = {
            'status': True,
            'error': False,
            'session_id': session_id,
            'msg' : "OK",
            'agent_resp' : agent_response
        }
        
        log.info("Agent Operation completed")
        return result
    
    except Exception as e:
        log.error("Error executing operation - " + str(e))
        result = {
                'status': False,
                'error' : True,
                'session_id': "",
                'msg' : f"Error - {str(e)}",
                'agent_resp' : ""
            }
        return result