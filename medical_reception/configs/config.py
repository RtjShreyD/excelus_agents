import os
import json
from dotenv import load_dotenv

def load_base_prompt():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    base_prompt_path = os.path.join(current_directory, "base_prompt.txt")

    try:
        with open(base_prompt_path, "r") as base_prompt_file:
            prompt_data = base_prompt_file.read()

        agent_details = agent_config.get('agent_details')
        prompt_data = prompt_data.format(**agent_details)

        return prompt_data

    except Exception as e:
        print(f"Error loading base prompt: {str(e)}")
        return None

def load_agent_config():
    current_directory = os.path.dirname(os.path.abspath(__file))
    json_file_path = os.path.join(current_directory, "agent_config.json")
    
    try:
        with open(json_file_path, "r") as json_file:
            config_data = json.load(json_file)
        return config_data

    except Exception as e:
        print(f"Error loading agent configuration: {str(e)}")
        return {}

def load_env_config():
    try:
        load_dotenv()
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

        envs = {
            "AUTH_SECRET_KEY": os.getenv('AUTH_SECRET_KEY'),
            "AUTH_ALGORITHM": os.getenv('AUTH_ALGORITHM'),
            "OPENAI_API_KEY": os.getenv('OPENAI_API_KEY'),
            "CELERY_BROKER_URL": os.getenv('CELERY_BROKER_URL'),
            "CELERY_RESULT_BACKEND": os.getenv('CELERY_RESULT_BACKEND'),
            "REDIS_MEMORY_SERVER_URL": os.getenv('REDIS_MEMORY_SERVER_URL'),
            "REDIS_DATA_SERVER_IP": os.getenv('REDIS_DATA_SERVER_IP'),
            "REDIS_DATA_SERVER_PORT": os.getenv('REDIS_DATA_SERVER_PORT'),
            "REDIS_DATA_SERVER_DB": os.getenv('REDIS_DATA_SERVER_DB')
        }
        return envs

    except Exception as e:
        print(f"Error loading environment variables: {str(e)}")
        return {}

# Load environment variables and configurations
agent_config = load_agent_config()
envs = load_env_config()

if not agent_config:
    print("Agent configuration is missing or invalid.")
    # You can choose to exit the program or handle it in another way.
if not envs:
    print("Error loading environment variables.")
    # You can choose to exit the program or handle it in another way.
