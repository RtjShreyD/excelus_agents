import redis
from configs.config import envs

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
        
        # Check if the key exists in the message_store
        return redis_conn.exists(key)