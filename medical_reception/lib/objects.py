from langchain.chat_models import ChatOpenAI
from configs.config import envs, agent_config
import redis
import os

llm = ChatOpenAI(model_name="gpt-4", temperature=0, verbose=True)

