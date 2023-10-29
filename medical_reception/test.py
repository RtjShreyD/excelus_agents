from lib.agent import MedicalReceptionAgent
import uuid

agent_instance = MedicalReceptionAgent()

session_id = str(uuid.uuid4())

resp = agent_instance.agent_begin(session_id)

print(resp)