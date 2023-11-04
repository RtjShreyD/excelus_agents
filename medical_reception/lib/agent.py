import datetime
import logging
from langchain.agents import initialize_agent
from lib.objects import llm
from lib.tools import create_toolkit
from langchain.memory.chat_message_histories.redis import RedisChatMessageHistory
from langchain.chains.conversation.memory import ConversationBufferMemory
from configs.config import envs, load_base_prompt, agent_config

class MedicalReceptionAgent:
    def __init__(self):
        self.agent_chain = self.initialize_base_agent()
        self.base_prompt = load_base_prompt()

    def initialize_base_agent(self):
        logging.info("Initializing memoryless base agent...Creating toolkit chain")
        toolkit = create_toolkit()
        logging.info("Initialized toolkit")
        agent_chain = initialize_agent(
            toolkit,
            llm,
            agent="conversational-react-description",
            memory=None,
            verbose=agent_config['agent_attributes']['verbose_mode']
        )
        logging.info("Initialized base agent")
        return agent_chain

    def _assign_memory(self, session_id):
        chat_history = RedisChatMessageHistory(
            url=envs['REDIS_MEMORY_SERVER_URL'],
            ttl=600,
            session_id=session_id
        )
        chat_history.add_user_message(
            f"session_id - {session_id}, today's date - {datetime.today().strftime('%Y-%m-%d')}, day of the week - {datetime.today().strftime('%A')}"
        )
        memory = ConversationBufferMemory(memory_key="chat_history", chat_memory=chat_history)
        self.agent_chain.memory = memory
        return chat_history, memory

    def _release_memory(self):
        self.agent_chain.memory = None

    def agent_begin(self, session_id):
        logging.info("Initializing agent session for session_id: " + str(session_id))
        chat_history, memory = self._assign_memory(session_id)

        logging.info("Assigned dynamic memory to agent chain...running base_chain")
        logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>> AGENT CHAIN START >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        agent_begin_resp = self.agent_chain.run(input=self.base_prompt)
        logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>> AGENT CHAIN END >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

        self._release_memory()
        chat_history.close()
        logging.info("Agent memory released")
        return agent_begin_resp

    def agent_chat(self, session_id, message):
        logging.info("Initializing agent chat for session_id: " + str(session_id))
        chat_history, memory = self._assign_memory(session_id)

        logging.info("Assigned dynamic memory to agent chain...running base_chain")
        logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>> AGENT CHAIN START >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        agent_chat_resp = self.agent_chain.run(input=message)
        logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>> AGENT CHAIN END >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

        self._release_memory()
        chat_history.close()
        logging.info("Agent memory released")
        return agent_chat_resp
