from langchain.agents import initialize_agent
from lib.objects import llm
from lib.tools import create_toolkit
from langchain.memory.chat_message_histories.redis import RedisChatMessageHistory
from langchain.chains.conversation.memory import ConversationBufferMemory
from configs.config import envs, load_base_prompt
from datetime import datetime


class MedicalReceptionAgent():
    def __init__(self):
        self.agent_chain = self.initialise_base_agent()
        self.base_prompt = load_base_prompt()

    def initialise_base_agent(self):
        print("Initialising memoryless base agent...Creating toolkit chain...")
        
        toolkit = create_toolkit()
        print("Initialised toolkit")
        
        agent_chain = initialize_agent(
            toolkit, 
            llm, 
            agent="conversational-react-description",
            memory=None, 
            verbose=True
        )
        print("Initialised base agent")
        
        return agent_chain
    

    def agent_begin(self, session_id, **kwargs):
        print("Initialising agent session for session_id: " + str(session_id))
        today_date = datetime.today().strftime('%Y-%m-%d')
        day_of_week = datetime.today().strftime('%A')

        chat_history = RedisChatMessageHistory(
            url=envs['REDIS_MEMORY_SERVER_URL'], 
            ttl=21600, # 6hrs 
            session_id=session_id
        )
        chat_history.add_user_message(f"session_id - {session_id}, today's date - {today_date}, day of the week - {day_of_week}")

        if kwargs.get('example') == True:
            agent_begin_resp = "This is an example Agent begin response, consider sending requests to initialise route for real agent response."

        else:
            memory = ConversationBufferMemory(memory_key="chat_history", chat_memory=chat_history)
            self.agent_chain.memory = memory

            print("Assigned dynamic memory to agent chain.....running base_chain")
            print(">>>>>>>>>>>>>>>>>>>>>>>>>> AGENT CHAIN START >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            agent_begin_resp = self.agent_chain.run(input=self.base_prompt)
            print(">>>>>>>>>>>>>>>>>>>>>>>>>> AGENT CHAIN END >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            self.agent_chain.memory = None
            print("Agent memory released")
        
        return agent_begin_resp

        
    def agent_chat(self, session_id, message, **kwargs):
        chat_history = RedisChatMessageHistory(
            url=envs['REDIS_MEMORY_SERVER_URL'], 
            ttl=21600, 
            session_id=session_id
        )

        if kwargs.get('example') == True:
            agent_chat_resp = "This is an example agent chat response, consider sending requests to chat route for real agent response."
        else:
            memory = ConversationBufferMemory(memory_key="chat_history", chat_memory=chat_history)
            self.agent_chain.memory = memory
            print("Assigned dynamic memory to agent chain.....running base_chain")
            print(">>>>>>>>>>>>>>>>>>>>>>>>>> AGENT CHAIN START >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            agent_chat_resp = self.agent_chain.run(input=message)
            print(">>>>>>>>>>>>>>>>>>>>>>>>>> AGENT CHAIN END >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            self.agent_chain.memory = None
        
        print("Agent memory released")
        return agent_chat_resp

        
        

