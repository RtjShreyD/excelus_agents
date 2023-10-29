from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.agents import Tool
from lib.objects import llm
from configs.config import agent_config
import importlib

def pre_processing_text(text_document_path):
    loader = TextLoader(text_document_path)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)
    return texts

def create_text_embedding(texts, collection_name):
    embeddings = OpenAIEmbeddings()
    docsearch = Chroma.from_documents(texts, embeddings, collection_name=collection_name)
    text_retrieval_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=docsearch.as_retriever())
    return text_retrieval_chain


def create_toolkit():
    tools = []

    #1. Create embedding tools
    embedding_tools_config = agent_config['embedding_tools']
    if embedding_tools_config and isinstance(embedding_tools_config, list):
        for item in embedding_tools_config:
            name = item['name']
            collection_name = item['collection_name']
            description = item['description']
            input_file_path = item['input_file_path']

            text_data = pre_processing_text(input_file_path)
            text_query_chain = create_text_embedding(text_data, collection_name)

            tools.append(
                Tool(
                    name=name,
                    func=text_query_chain.run,
                    description=description,
                )
            )
            print(f"Added tool - {name}")
    else:
        print("No embedding tool configured")

    
    #2. Add custom tools
    functional_tools_config = agent_config['custom_functional_tools']
    
    if functional_tools_config and isinstance(functional_tools_config, list):
        custom_tools_module_name = "lib.custom_tools"
        custom_tools_module = importlib.import_module(custom_tools_module_name)

        for item in functional_tools_config:
            name = item['name']
            function_name = item['function_name']
            description = item['description']
            if hasattr(custom_tools_module, function_name):
                function = getattr(custom_tools_module, function_name)
                tools.append(
                    Tool(
                        name=name,
                        func=function,
                        description=description
                    )
                )
                print(f"Added tool - {name}")
            else:
                print("Unknown function from custom_tools_module")
    else:
        print("No custom functionaltool configured")

    return tools