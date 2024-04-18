from langchain.agents import initialize_agent
from lib.objects import llm
from lib.tools import create_toolkit
from langchain.memory.chat_message_histories.redis import RedisChatMessageHistory
from langchain.chains.conversation.memory import ConversationBufferMemory
from configs.config import envs, load_base_prompt
from datetime import datetime


class MedicalReceptionAgent():
    def __init__(self):
        self.toolkit = create_toolkit()
        self.agent_chain = self.initialise_base_agent()
        self.agent_stream_chain = self.initialise_base_agent_stream()
        self.base_prompt = load_base_prompt()
        
        print("Initialised toolkit")

    
    def initialise_base_agent_stream(self):
        print("Initialising memoryless base agent with streaming...Creating toolkit chain...")
        
        agent_chain = initialize_agent(
            self.toolkit, 
            llm, 
            agent="conversational-react-description",
            memory=None, 
            verbose=True,
            handle_parsing_errors="Do not run into Could not parse LLM output: `Do I need to use a tool?` loop more that two times.Also handle other errors.",     # for handling parsing errors, used with gpt-3.5-turbo
            maximum_execution_time=2,
            streaming=True
        )
        print("Initialised base agent")
        
        return agent_chain
    

    def agent_begin_stream(self, session_id):
        print("Initialising agent session for session_id: " + str(session_id))
        today_date = datetime.today().strftime('%Y-%m-%d')
        day_of_week = datetime.today().strftime('%A')

        chat_history = RedisChatMessageHistory(
            url=envs['REDIS_MEMORY_SERVER_URL'], 
            ttl=21600,
            session_id=session_id
        )
        chat_history.add_user_message(f"session_id - {session_id}, today's date - {today_date}, day of the week - {day_of_week}")

        memory = ConversationBufferMemory(memory_key="chat_history", chat_memory=chat_history)
        self.agent_chain.memory = memory

        print("Assigned dynamic memory to agent chain.....running base_chain")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>> AGENT CHAIN START >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

        for chunk in self.agent_chain.run(self.base_prompt):
            yield chunk
        
        self.agent_chain.memory = None
        print("\nAgent memory released")

    
    def agent_chat_stream(self, session_id, message):
        chat_history = RedisChatMessageHistory(
            url=envs['REDIS_MEMORY_SERVER_URL'], 
            ttl=21600, 
            session_id=session_id
        )

        memory = ConversationBufferMemory(memory_key="chat_history", chat_memory=chat_history)
        self.agent_chain.memory = memory
        print("Assigned dynamic memory to agent chain.....running base_chain")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>> AGENT CHAIN START >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        for chunk in self.agent_chain.run(input=message):
            yield chunk
        
        self.agent_chain.memory = None
        print("\nAgent memory released")
        

    def initialise_base_agent(self):
        print("Initialising memoryless base agent...Creating toolkit chain...")
        
        agent_chain = initialize_agent(
            self.toolkit, 
            llm, 
            agent="conversational-react-description",
            memory=None, 
            verbose=True,
            handle_parsing_errors=True,     # for handling parsing errors, used with gpt-3.5-turbo
            maximum_execution_time=3
        )
        print("Initialised base agent")
        
        return agent_chain
    

    def agent_begin(self, session_id):
        print("Initialising agent session for session_id: " + str(session_id))
        today_date = datetime.today().strftime('%Y-%m-%d')
        day_of_week = datetime.today().strftime('%A')

        chat_history = RedisChatMessageHistory(
            url=envs['REDIS_MEMORY_SERVER_URL'], 
            ttl=21600, # 6hrs 
            session_id=session_id
        )
        chat_history.add_user_message(f"session_id - {session_id}, today's date - {today_date}, day of the week - {day_of_week}")

        memory = ConversationBufferMemory(memory_key="chat_history", chat_memory=chat_history)
        self.agent_chain.memory = memory

        print("Assigned dynamic memory to agent chain.....running base_chain")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>> AGENT CHAIN START >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        agent_begin_resp = self.agent_chain.run(input=self.base_prompt)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>> AGENT CHAIN END >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        self.agent_chain.memory = None
        print("Agent memory released")
        return agent_begin_resp

        
    def agent_chat(self, session_id, message):
        chat_history = RedisChatMessageHistory(
            url=envs['REDIS_MEMORY_SERVER_URL'], 
            ttl=21600, 
            session_id=session_id
        )

        memory = ConversationBufferMemory(memory_key="chat_history", chat_memory=chat_history)
        self.agent_chain.memory = memory
        print("Assigned dynamic memory to agent chain.....running base_chain")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>> AGENT CHAIN START >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        agent_chat_resp = self.agent_chain.run(input=message)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>> AGENT CHAIN END >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        self.agent_chain.memory = None
        print("Agent memory released")
        return agent_chat_resp

        
        

