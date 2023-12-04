import redis
import random
from celery.result import AsyncResult
from configs.config import envs

processing_messages = [
    "Thank you. Processing your request.",
    "We're on it. Will update you soon.",
    "Your query is being handled. Thanks!",
    "Processing your request. Thank you!",
    "Thanks for reaching out. Processing now."
]

failure_messages = [
    "Apologies. Something went wrong. We're investigating.",
    "We encountered an issue. Our team is on it.",
    "Sorry, there was an error. We're working to fix it.",
    "Oops! An error occurred. We're addressing it now.",
    "We apologize for the inconvenience. Our team is resolving the issue."
]

def get_random_processing_message():
    return random.choice(processing_messages)

def get_random_failure_message():
    return random.choice(failure_messages)


class InfoHandler:
    def __init__(self):
        self.redis_connections = {}

    def _get_redis_connection(self, db_name):
        if db_name not in self.redis_connections:
            connection_string = self._get_redis_connection_string(db_name)
            self.redis_connections[db_name] = redis.StrictRedis.from_url(connection_string)
        return self.redis_connections[db_name]

    def _get_redis_connection_string(self, db_name):
        connection_mapping = {
            'MEMORY_SERVER': envs['REDIS_MEMORY_SERVER_URL'],
            'RESULT_BACKEND': envs['CELERY_RESULT_BACKEND'],
            'REDIS_DATA_SERVER': envs['REDIS_DATA_SERVER_URL'],
           
        }
        return connection_mapping.get(db_name, None)

    
    def is_registered_session(self, session_id):
        redis_conn = self._get_redis_connection('MEMORY_SERVER')
        key = f'message_store:{session_id}'
        
        return redis_conn.exists(key)
    

    def get_task_result(self, task_id):
        try:
            result = AsyncResult(task_id)
            if result.ready():
                print("Worker has finished the task")
                return result.result
            else:
                print("Worker has not picked up the task, or task is in progress")
                return None
        except Exception as e:
            print(f"Error retrieving task result for {task_id}: {e}")
            return None
    

    def check_response(self, task_id):
        resp = self.get_task_result(task_id)
        if resp is not None:
            status = resp.get('status')
            if status == True:
                print("Status: %s" % status)
                agent_response = resp.get('agent_resp')
                
            else:
                print("Status: %s" % status)
                agent_response = get_random_failure_message()
                
        else:
            agent_response = get_random_processing_message()

        return agent_response