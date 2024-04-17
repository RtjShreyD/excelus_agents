from langchain.chat_models import ChatOpenAI
from configs.config import envs, agent_config
import redis
import os

llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, verbose=True)

