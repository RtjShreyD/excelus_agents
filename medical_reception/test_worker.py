from celery import Celery
from workers.operations import operator  
from dotenv import load_dotenv
import os

load_dotenv()

app = Celery(__name__)

app.conf.broker_url = os.environ.get("CELERY_BROKER_URL")
app.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND")

obj = {
    'session_id': "123456",
}


def publish_task(input_dict):
    try:
        result = operator.apply_async(args=[input_dict])
        print(f"Task {result.id} published successfully.")
    except Exception as e:
        print(f"Failed to publish task: {e}")

# Example usage
if __name__ == "__main__":
    publish_task(obj)
