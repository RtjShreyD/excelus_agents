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
    try:
        loader = TextLoader(text_document_path)
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
        texts = text_splitter.split_documents(documents)
        return texts
    except Exception as e:
        print(f"Error in pre_processing_text: {str(e)}")
        return []

def create_text_embedding(texts, collection_name):
    try:
        embeddings = OpenAIEmbeddings()
        docsearch = Chroma.from_documents(texts, embeddings, collection_name=collection_name)
        text_retrieval_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=docsearch.as_retriever())
        return text_retrieval_chain
    except Exception as e:
        print(f"Error in create_text_embedding: {str(e)}")
        return None

def create_toolkit():
    tools = []

    # 1. Create embedding tools
    embedding_tools_config = agent_config.get('embedding_tools', [])
    for item in embedding_tools_config:
        name = item.get('name')
        collection_name = item.get('collection_name')
        description = item.get('description')
        input_file_path = item.get('input_file_path')

        text_data = pre_processing_text(input_file_path)
        if text_data:
            text_query_chain = create_text_embedding(text_data, collection_name)
            if text_query_chain:
                tools.append(Tool(name=name, func=text_query_chain.run, description=description))
                print(f"Added tool - {name}")
            else:
                print(f"Error creating text embedding for {name}")
        else:
            print(f"Error processing text data for {name}")

    # 2. Add custom tools
    functional_tools_config = agent_config.get('custom_functional_tools', [])
    custom_tools_module_name = "lib.custom_tools"
    custom_tools_module = importlib.import_module(custom_tools_module_name)

    for item in functional_tools_config:
        name = item.get('name')
        function_name = item.get('function_name')
        description = item.get('description')
        if hasattr(custom_tools_module, function_name):
            function = getattr(custom_tools_module, function_name)
            tools.append(Tool(name=name, func=function, description=description))
            print(f"Added tool - {name}")
        else:
            print(f"Unknown function from custom_tools_module for {name}")

    return tools

if __name__ == "__main":
    toolkit = create_toolkit()
    if not toolkit:
        print("Error creating the toolkit")
