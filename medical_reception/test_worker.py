from celery import Celery
from workers.operations import operator, ask_agent
from dotenv import load_dotenv
import os

load_dotenv()

app = Celery(__name__)

app.conf.broker_url = os.environ.get("CELERY_BROKER_URL")
app.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND")

obj = {
    'session_id': "7a76d2",
    'call_sid' : "7a76d2",
    'query': "I have fever recommend me some doctor"
}


def publish_task(input_dict):
    try:
        result = ask_agent.apply_async(args=[input_dict])
        print(f"Task {result.id} published successfully.")
    except Exception as e:
        print(f"Failed to publish task: {e}")


if __name__ == "__main__":
    publish_task(obj)
