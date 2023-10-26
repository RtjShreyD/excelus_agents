from celery import Celery
import logging
import os
import time
from dotenv import load_dotenv

load_dotenv()

log = logging.getLogger(__name__)

app = Celery(__name__)
app.conf.broker_url = os.environ.get("CELERY_BROKER_URL")
app.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND")
app.conf.broker_connection_retry = True
app.conf.acks_late=True


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