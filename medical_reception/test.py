from lib.agent import MedicalReceptionAgent
import uuid

agent_instance = MedicalReceptionAgent()

session_id = str(uuid.uuid4())
print("Session ID: " + session_id)

# resp = agent_instance.agent_begin(session_id)
# print(resp)

# message = "Hi Uday, I have some fever please recommend me a doctor"
# resp = agent_instance.agent_chat(session_id, message)
# print(resp)

message = "Please make my booking with any doctor at the earliest possible time today"
# resp = agent_instance.agent_chat(session_id, message)
# print(resp)

# Begin the agent streaming session
print("Starting agent streaming session...")
for chunk in agent_instance.agent_begin_stream(session_id):
    print(chunk, end=' ')

for chunk in agent_instance.agent_chat_stream(session_id, message):
    print(chunk, end=' ')

print("Agent streaming session completed.")