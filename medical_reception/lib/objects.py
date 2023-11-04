from langchain.chat_models import ChatOpenAI
from configs.config import envs, agent_config
import redis
import os

agent_model_name = agent_config['agent_attributes']['model_name']
verbose_mode = agent_config['agent_attributes']['verbose_mode']

llm = ChatOpenAI(model_name=agent_model_name, temperature=0, verbose=verbose_mode)

